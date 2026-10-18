#!/usr/bin/env python3
"""Pruebas de bowser-ai-lite contra el OpenCode real (el que esté en el PATH). No gasta tokens.

Uso: python3 pruebas/opencode_real.py

Instala el kit en un proyecto temporal y le pregunta a OpenCode qué cargó (`opencode debug config` y
`opencode debug skill`): comandos, agentes, modelos, permisos y skills. Sirve para saber si una versión de
OpenCode lee el kit como esperamos, sin abrir la interfaz.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT))
import instalar  # noqa: E402

FALLOS: list[str] = []


def caso(nombre: str, condicion: bool, detalle: object = "") -> None:
    print(("  ✓ " if condicion else "  ✗ ") + nombre + ("" if condicion else f"  ({detalle})"))
    if not condicion:
        FALLOS.append(nombre)


def opencode_json(proyecto: Path, *args: str):
    # A un archivo: algunas versiones cortan el JSON grande cuando escriben a una tubería.
    with tempfile.TemporaryFile("w+", encoding="utf-8") as salida:
        r = subprocess.run(["opencode", *args], cwd=proyecto, stdout=salida, stderr=subprocess.PIPE, text=True, timeout=180)
        salida.seek(0)
        texto = salida.read()
    if r.returncode != 0:
        raise RuntimeError(f"opencode {' '.join(args)} falló: {r.stderr.strip()[:300]}")
    inicio = min(i for i in (texto.find("{"), texto.find("[")) if i >= 0)
    return json.loads(texto[inicio:])


def frontmatter(ruta: Path) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---", ruta.read_text(encoding="utf-8"), re.S)
    campos = {}
    for linea in (m.group(1) if m else "").splitlines():
        if ":" in linea and not linea.startswith(" "):
            k, v = linea.split(":", 1)
            campos[k.strip()] = v.strip().strip('"')
    return campos


def main() -> int:
    try:
        version = subprocess.run(["opencode", "--version"], capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        print("✗ No está el programa 'opencode' en el PATH.", file=sys.stderr)
        return 2
    print(f"OpenCode {version}")

    skills = sorted(d.name for d in (KIT / "catalogo").iterdir() if (d / "SKILL.md").exists())
    comandos = {Path(r).stem: KIT / "plantilla" / r for r in instalar.DEL_KIT if r.startswith(".opencode/commands/")}
    agentes = {Path(r).stem: KIT / "plantilla" / r for r in instalar.DEL_KIT if r.startswith(".opencode/agents/")}

    with tempfile.TemporaryDirectory(prefix="bowser-oc-") as tmp:
        p = Path(tmp)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=p, check=True)
        r = subprocess.run([sys.executable, str(KIT / "bin/bowser"), "init", "--skills", ",".join(skills)], cwd=p,
                           capture_output=True, text=True)
        caso("bowser init instala el kit", r.returncode == 0, r.stderr)
        try:
            cfg = opencode_json(p, "debug", "config")
        except (RuntimeError, ValueError) as e:
            caso("OpenCode acepta la configuración del kit", False, e)
            return 1
        caso("OpenCode acepta la configuración del kit", True)

        print("Comandos")
        cargados = cfg.get("command") or {}
        for nombre, archivo in sorted(comandos.items()):
            caso(f"/{nombre} está disponible", nombre in cargados, sorted(cargados))
            esperado = frontmatter(archivo).get("agent")
            if nombre in cargados and esperado:
                caso(f"/{nombre} corre con el agente {esperado}", cargados[nombre].get("agent") == esperado, cargados[nombre].get("agent"))
        sobran = sorted(set(cargados) - set(comandos))
        caso("no hay comandos de más", not sobran, sobran)

        print("Agentes")
        caso("el agente por defecto es constructor", cfg.get("default_agent") == "constructor", cfg.get("default_agent"))
        cargados = cfg.get("agent") or {}
        for nombre, archivo in sorted(agentes.items()):
            fm = frontmatter(archivo)
            a = cargados.get(nombre) or {}
            caso(f"@{nombre} está disponible", bool(a), sorted(cargados))
            caso(f"@{nombre} usa {fm.get('model')}", a.get("model") == fm.get("model"), a.get("model"))
            caso(f"@{nombre} es {fm.get('mode')}", a.get("mode") == fm.get("mode"), a.get("mode"))
        perm = (cargados.get("constructor") or {}).get("permission") or {}
        bash = perm.get("bash") if isinstance(perm.get("bash"), dict) else {}
        caso("el constructor pregunta antes de git push", bash.get("git push*") == "ask", bash)
        caso("el constructor corre comandos sin preguntar", bash.get("*") == "allow", bash)
        perm_rev = (cargados.get("revisor") or {}).get("permission") or {}
        caso("el revisor no puede editar", perm_rev.get("edit") == "deny", perm_rev)

        print("Skills")
        try:
            vistas = {s.get("name") for s in opencode_json(p, "debug", "skill")}
        except (RuntimeError, ValueError) as e:
            caso("OpenCode lista las skills", False, e)
            vistas = set()
        for nombre in skills:
            caso(f"la skill {nombre} está disponible", nombre in vistas, sorted(vistas))

    print()
    if FALLOS:
        print(f"✗ {len(FALLOS)} pruebas fallaron con OpenCode {version}: " + "; ".join(FALLOS))
        return 1
    print(f"✓ OpenCode {version} carga el kit como se espera.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
