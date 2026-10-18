#!/usr/bin/env python3
"""bowser-ai-lite · Comprueba que la rama actual se puede cerrar. No depende de que el agente obedezca.

Uso: python3 .bowser/verificar.py [--base RAMA] [--sin-check] [--ci]

Comprueba, contra la rama principal:
  1. Que `make check` pasa (salvo --sin-check).
  2. Que si cambió código, también cambiaron pruebas, o algún commit explica por qué no con `Sin-pruebas: <motivo>`.
  3. Que si tocó archivos riesgosos, la rama tiene un plan de tamaño grande, commiteado antes que esos archivos.
  4. Que el agente revisor revisó la rama (leyendo las sesiones de OpenCode). En --ci no se comprueba.
  5. Avisa si la memoria pudo quedar vieja: la rama tocó algo y no actualizó el archivo de docs/memoria que lo
     describe, o creó una carpeta de código nueva sin tocar arquitectura.md. Cuenta lo que aún no se commiteó.
Los patrones de 2, 3 y 5 están en .bowser/verificacion, que es del proyecto.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def leer_config() -> dict[str, list[str]]:
    secciones: dict[str, list[str]] = {"pruebas": [], "riesgo": [], "no-codigo": [], "memoria": []}
    actual = None
    archivo = RAIZ / ".bowser/verificacion"
    if not archivo.exists():
        return secciones
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        m = re.fullmatch(r"\[(.+)\]", linea)
        if m:
            actual = m.group(1).strip().lower()
            secciones.setdefault(actual, [])
        elif actual:
            secciones[actual].append(linea)
    return secciones


def coincide(ruta: str, patrones: list[str]) -> bool:
    return any(fnmatch(ruta, p) or fnmatch(Path(ruta).name, p) for p in patrones)


def rama_base(pedida: str | None) -> str:
    if pedida:
        return pedida
    for candidata in ("main", "master", "origin/main", "origin/master"):
        if git("rev-parse", "--verify", "--quiet", candidata):
            return candidata
    return ""


class Informe:
    def __init__(self) -> None:
        self.fallos = 0

    def bien(self, texto: str) -> None:
        print(f"  ✓ {texto}")

    def aviso(self, texto: str) -> None:
        print(f"  ⚠ {texto}")

    def mal(self, texto: str) -> None:
        print(f"  ✗ {texto}")
        self.fallos += 1


def comprobar_check(inf: Informe) -> None:
    r = subprocess.run(["make", "check"], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode == 0:
        inf.bien("make check pasa")
    else:
        salida = (r.stdout + r.stderr).strip().splitlines()[-8:]
        inf.mal("make check falla:\n      " + "\n      ".join(salida))


def comprobar_pruebas(inf: Informe, cfg: dict, base: str, archivos: list[str]) -> None:
    codigo = [f for f in archivos if not coincide(f, cfg["no-codigo"]) and not coincide(f, cfg["pruebas"])]
    pruebas = [f for f in archivos if coincide(f, cfg["pruebas"])]
    if not codigo:
        inf.bien("la rama no cambia código")
        return
    if pruebas:
        inf.bien(f"cambia código ({len(codigo)} archivos) y pruebas ({len(pruebas)})")
        return
    motivos = re.findall(r"^Sin-pruebas:\s*(.+)$", git("log", "--format=%B", f"{base}..HEAD"), re.MULTILINE)
    if motivos:
        inf.aviso(f"cambia código sin pruebas, con motivo: {motivos[-1].strip()}")
        return
    inf.mal("cambia código sin cambiar pruebas: " + ", ".join(codigo[:5]) + (" …" if len(codigo) > 5 else "") +
            "\n      Agrega la prueba, o explica en un commit por qué no aplica: `Sin-pruebas: <motivo>`.")


def comprobar_tamano(inf: Informe, cfg: dict, base: str, archivos: list[str], rama: str) -> None:
    riesgosos = [f for f in archivos if coincide(f, cfg["riesgo"]) and not f.endswith(".md")]
    if not riesgosos:
        inf.bien("no toca archivos riesgosos")
        return
    nombre = rama.split("/", 1)[-1]
    plan = f"docs/cambios/{nombre}.md"
    lista = ", ".join(riesgosos[:4]) + (" …" if len(riesgosos) > 4 else "")
    ruta = RAIZ / plan
    if not ruta.exists() or plan not in archivos:
        inf.mal(f"toca archivos riesgosos ({lista}) y la rama no tiene plan en {plan}.\n"
                "      Un cambio así es grande: plan y aprobación antes de programar.")
        return
    if not any("tamaño" in l.lower() and "grande" in l.lower() for l in ruta.read_text(encoding="utf-8").splitlines()):
        inf.mal(f"toca archivos riesgosos ({lista}) y {plan} no dice «Tamaño: grande».")
        return
    commit_plan = git("log", "--diff-filter=A", "--format=%H", f"{base}..HEAD", "--", plan).splitlines()
    commits_riesgo = git("log", "--reverse", "--format=%H", f"{base}..HEAD", "--", *riesgosos).splitlines()
    if commit_plan and commits_riesgo:
        primero_plan, primero_riesgo = commit_plan[-1], commits_riesgo[0]
        antes = primero_plan != primero_riesgo and subprocess.run(
            ["git", "merge-base", "--is-ancestor", primero_plan, primero_riesgo], cwd=RAIZ).returncode == 0
        if not antes:
            inf.mal(f"el plan {plan} se commiteó junto con o después de los archivos riesgosos: va primero.")
            return
    inf.bien(f"toca archivos riesgosos y tiene plan grande previo ({plan})")


def comprobar_revision(inf: Informe, base: str, archivos: list[str], cfg: dict) -> None:
    import costo  # mismo directorio: lee las sesiones de OpenCode

    desde, _ = costo.inicio_de_rama()
    try:
        sesiones = [s for s in costo.sesiones_del_proyecto() if (s.get("updated") or s.get("created") or 0) >= desde]
        vistas, pendientes, ultima = set(), [s["id"] for s in sesiones if s.get("id")], 0
        while pendientes:
            sid = pendientes.pop()
            if sid in vistas:
                continue
            vistas.add(sid)
            exp = costo.exportar(sid)
            for r in costo.respuestas(exp):
                if r["agente"] == "revisor" and r["ms"] >= desde:
                    ultima = max(ultima, r["ms"])
            pendientes += costo.hijas(exp)
    except costo.Fallo as e:
        inf.mal(f"no se pudo comprobar la revisión en las sesiones de OpenCode: {e}")
        return
    if not ultima:
        inf.mal("el agente revisor no revisó esta rama. Pide /bowser-review antes de cerrar.")
        return
    codigo = [f for f in archivos if not coincide(f, cfg["no-codigo"])]
    ultimo_cambio = git("log", "-1", "--format=%ct", f"{base}..HEAD", "--", *codigo) if codigo else ""
    if ultimo_cambio and int(ultimo_cambio) * 1000 > ultima:
        inf.aviso("hubo cambios de código después de la última revisión; si no son menores, pide otra.")
    else:
        inf.bien("el revisor revisó la rama")


def comprobar_memoria(inf: Informe, cfg: dict, base: str, archivos: list[str]) -> None:
    pendientes = git("diff", "--name-only", base).splitlines() + git("ls-files", "--others", "--exclude-standard").splitlines()
    tocados = set(archivos) | set(pendientes)
    avisos = []
    for regla in cfg["memoria"]:
        if "->" not in regla:
            continue
        patron, memoria = (x.strip() for x in regla.split("->", 1))
        coinciden = [f for f in tocados if coincide(f, [patron]) and not f.endswith(".md")]
        if coinciden and memoria not in tocados:
            avisos.append(f"cambió {coinciden[0]}{' y otros' if len(coinciden) > 1 else ''} y no se actualizó {memoria}")
    nuevos = git("diff", "--name-only", "--diff-filter=A", base).splitlines() + git("ls-files", "--others", "--exclude-standard").splitlines()
    carpetas = set()
    for f in nuevos:
        if coincide(f, cfg["no-codigo"]) or coincide(f, cfg["pruebas"]) or "/" not in f:
            continue
        partes = f.split("/")[:-1]
        for i in range(1, len(partes) + 1):
            carpeta = "/".join(partes[:i])
            if subprocess.run(["git", "cat-file", "-e", f"{base}:{carpeta}"], cwd=RAIZ, capture_output=True).returncode != 0:
                carpetas.add(carpeta)
                break
    if carpetas and "docs/memoria/arquitectura.md" not in tocados:
        avisos.append(f"hay carpetas de código nuevas ({', '.join(sorted(carpetas)[:3])}) y no se actualizó docs/memoria/arquitectura.md")
    for a in sorted(avisos):
        inf.aviso("memoria: " + a)
    if not avisos:
        inf.bien("la memoria acompaña los cambios")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", help="rama principal contra la que se compara (por defecto main o master)")
    ap.add_argument("--sin-check", action="store_true", help="no corre make check")
    ap.add_argument("--ci", action="store_true", help="en CI: sin make check ni revisión (no hay sesiones de OpenCode)")
    a = ap.parse_args()

    base = rama_base(a.base)
    rama = git("rev-parse", "--abbrev-ref", "HEAD")
    if not base:
        print("✗ No encontré la rama principal (main o master). Usa --base.", file=sys.stderr)
        return 1
    if not a.ci and rama in ("main", "master"):
        print("✗ Estás en la rama principal: la verificación es de una rama de funcionalidad.", file=sys.stderr)
        return 1
    if a.ci and rama == "HEAD":
        rama = os.environ.get("GITHUB_HEAD_REF", "")
    punto = git("merge-base", base, "HEAD")
    archivos = git("diff", "--name-only", f"{punto}..HEAD").splitlines() if punto else []
    cfg = leer_config()

    print(f"Verificación de la rama {rama} contra {base} · {len(archivos)} archivos cambiados")
    inf = Informe()
    if not (a.sin_check or a.ci):
        comprobar_check(inf)
    comprobar_pruebas(inf, cfg, punto, archivos)
    comprobar_tamano(inf, cfg, punto, archivos, rama)
    if not a.ci:
        comprobar_revision(inf, punto, archivos, cfg)
        comprobar_memoria(inf, cfg, punto, archivos)
    print()
    if inf.fallos:
        print(f"✗ La rama no se puede cerrar todavía ({inf.fallos} pendiente{'s' if inf.fallos > 1 else ''}). "
              "Corrige la causa; no cambies .bowser/verificacion para que pase.")
        return 1
    print("✓ La rama se puede cerrar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
