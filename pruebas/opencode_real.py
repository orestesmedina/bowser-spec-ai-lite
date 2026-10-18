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


def opencode_json(proyecto: Path, *args: str, tipo: type = dict):
    """El primer valor JSON del tipo esperado en la salida (algunas versiones escriben otras líneas antes)."""
    # A un archivo: algunas versiones cortan el JSON grande cuando escriben a una tubería.
    with tempfile.TemporaryFile("w+", encoding="utf-8") as salida:
        r = subprocess.run(["opencode", *args], cwd=proyecto, stdout=salida, stderr=subprocess.PIPE, text=True, timeout=180)
        salida.seek(0)
        texto = salida.read()
    if r.returncode != 0:
        raise RuntimeError(f"opencode {' '.join(args)} falló: {r.stderr.strip()[:300]}")
    decodificador = json.JSONDecoder()
    for i, c in enumerate(texto):
        if c in "{[":
            try:
                valor, _ = decodificador.raw_decode(texto, i)
            except ValueError:
                continue
            if isinstance(valor, tipo):
                return valor
    raise ValueError(f"opencode {' '.join(args)} no devolvió un JSON {tipo.__name__}. Empieza así: {texto[:400]!r}")


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
        if mayor(version) >= 2:
            return opencode_2(p, version, comandos, agentes, skills)
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
            vistas = {s.get("name") for s in opencode_json(p, "debug", "skill", tipo=list) if isinstance(s, dict)}
        except (RuntimeError, ValueError) as e:
            caso("OpenCode lista las skills", False, e)
            vistas = set()
        for nombre in skills:
            caso(f"la skill {nombre} está disponible", nombre in vistas, sorted(vistas))

    return resultado(version)


def resultado(version: str, sin_comprobar: list[str] | None = None) -> int:
    print()
    if FALLOS:
        print(f"✗ {len(FALLOS)} pruebas fallaron con OpenCode {version}: " + "; ".join(FALLOS))
        return 1
    print(f"✓ OpenCode {version} carga el kit como se espera.")
    if sin_comprobar:
        print("  Sin comprobar en esta versión (no hay forma de preguntárselo sin abrir la interfaz): " + ", ".join(sin_comprobar) + ".")
    return 0


def mayor(version: str) -> int:
    m = re.search(r"(\d+)\.\d+", version)
    return int(m.group(1)) if m else 0


def permiso(agente: dict, accion: str, recurso: str) -> str | None:
    """El efecto de la última regla de OpenCode 2 para esa acción y ese patrón (la última manda)."""
    efecto = None
    for regla in agente.get("permissions") or []:
        if regla.get("action") == accion and regla.get("resource") == recurso:
            efecto = regla.get("effect")
    return efecto


def opencode_2(p: Path, version: str, comandos: dict, agentes: dict, skills: list[str]) -> int:
    """OpenCode 2.x: `debug config` lista de dónde lee la configuración y `debug agents` los agentes cargados.
    No tiene forma de listar comandos ni skills desde la terminal."""
    try:
        fuentes = opencode_json(p, "debug", "config", tipo=list)
    except (RuntimeError, ValueError) as e:
        caso("OpenCode acepta la configuración del kit", False, e)
        return 1
    caso("OpenCode acepta la configuración del kit", True)
    rutas = {Path(f.get("path", "")).resolve() for f in fuentes if isinstance(f, dict)}
    caso("OpenCode lee la carpeta .opencode del proyecto", (p / ".opencode").resolve() in rutas, sorted(map(str, rutas)))
    proyecto = next((f.get("info") or {} for f in fuentes if isinstance(f, dict)
                     and Path(f.get("path", "")).resolve() == (p / "opencode.json").resolve()), {})
    caso("el agente por defecto es constructor", proyecto.get("default_agent") == "constructor", proyecto.get("default_agent"))

    print("Agentes")
    # OpenCode 2 responde desde un servicio de fondo que no lee los agentes de una carpeta nueva hasta `opencode reload`.
    subprocess.run(["opencode", "reload"], cwd=p, capture_output=True, text=True, timeout=60)
    try:
        cargados = {a.get("id"): a for a in opencode_json(p, "debug", "agents", tipo=list) if isinstance(a, dict)}
    except (RuntimeError, ValueError) as e:
        caso("OpenCode lista los agentes", False, e)
        cargados = {}
    for nombre, archivo in sorted(agentes.items()):
        fm = frontmatter(archivo)
        a = cargados.get(nombre) or {}
        modelo = a.get("model") or {}
        caso(f"@{nombre} está disponible", bool(a), sorted(k for k in cargados if k))
        caso(f"@{nombre} usa {fm.get('model')}", f"{modelo.get('providerID')}/{modelo.get('id')}" == fm.get("model"), modelo)
        caso(f"@{nombre} es {fm.get('mode')}", a.get("mode") == fm.get("mode"), a.get("mode"))
    constructor, revisor = cargados.get("constructor") or {}, cargados.get("revisor") or {}
    caso("el constructor pregunta antes de git push", permiso(constructor, "shell", "git push*") == "ask", permiso(constructor, "shell", "git push*"))
    caso("el constructor corre comandos sin preguntar", permiso(constructor, "shell", "*") == "allow", permiso(constructor, "shell", "*"))
    caso("el revisor no puede editar", permiso(revisor, "edit", "*") == "deny", permiso(revisor, "edit", "*"))
    return resultado(version, ["los comandos /bowser-*", "las skills"])


if __name__ == "__main__":
    sys.exit(main())
