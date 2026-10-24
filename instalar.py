#!/usr/bin/env python3
"""bowser-ai-lite · Instala o actualiza el kit en un proyecto.

Uso:
  python3 instalar.py <carpeta-del-proyecto>             instalar o actualizar
  python3 instalar.py <carpeta-del-proyecto> --verificar  solo decir qué cambiaría (no escribe nada)
  python3 instalar.py <carpeta-del-proyecto> --forzar     reemplazar también los archivos del kit editados en el proyecto
                                                          (deja una copia en .bowser/respaldo/)

Dos tipos de archivo (ver README.md):
  - Del kit: se reemplazan al actualizar. Si el proyecto editó uno, no se toca y se avisa.
  - Semillas: se copian solo si no existen. Desde entonces son del proyecto.
Solo biblioteca estándar de Python 3.9+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
PLANTILLA = KIT / "plantilla"
CATALOGO = KIT / "catalogo"
MANIFIESTO = ".bowser/kit.json"

DEL_KIT = [
    ".opencode/agents/constructor.md",
    ".opencode/agents/revisor.md",
    ".opencode/agents/explorador.md",
    ".opencode/commands/bowser-feature.md",
    ".opencode/commands/bowser-review.md",
    ".opencode/commands/bowser-close.md",
    ".opencode/commands/bowser-cost.md",
    ".opencode/commands/bowser-resume.md",
    ".opencode/commands/bowser-idea.md",
    ".opencode/commands/bowser-roadmap.md",
    ".opencode/commands/bowser-update.md",
    ".opencode/commands/bowser-discover.md",
    ".githooks/pre-commit",
    ".githooks/commit-msg",
    ".githooks/pre-push",
    ".bowser/verificar.py",
    ".bowser/costo.py",
    ".bowser/principios.md",
    ".bowser/documentacion.md",
    ".bowser/estandares.md",
    ".github/workflows/bowser.yml",
    "bowser.mk",
]

SEMILLAS = [
    "AGENTS.md",
    "Makefile",
    "opencode.json",
    ".bowser/inmutables",
    ".bowser/skills",
    ".bowser/verificacion",
    ".bowser/versiones",
    "docs/memoria/producto.md",
    "docs/memoria/arquitectura.md",
    "docs/memoria/modulos.md",
    "docs/memoria/base-de-datos.md",
    "docs/memoria/decisiones.md",
    "docs/memoria/trampas.md",
    "docs/memoria/convenciones.md",
    "docs/memoria/deuda.md",
    "docs/producto/requerimientos.md",
    "docs/producto/roadmap.md",
    "docs/producto/historial.md",
]

# En el kit, algunos archivos se guardan con otro nombre (un Makefile o un workflow de GitHub dentro del kit
# se ejecutarían como si fueran del kit). Aquí: ruta en el proyecto -> ruta en plantilla/.
FUENTE = {"Makefile": "Makefile.plantilla", ".github/workflows/bowser.yml": "github/bowser.yml"}


def fuente(rel: str) -> Path:
    return PLANTILLA / FUENTE.get(rel, rel)


GITIGNORE = ["# bowser-ai-lite: secretos", ".env", ".env.*", "!.env.example", ".bowser/respaldo/"]
INCLUDE = "-include bowser.mk"
# Makefiles de la plantilla de versiones anteriores, sin tocar. Un proyecto que lo tiene así no lo hizo suyo todavía,
# y se le pone la plantilla nueva. Hasta 0.13.0, test y lint fallaban sin definir y bloqueaban el primer push.
MAKEFILES_VIEJOS = {"5bf943767b4ce486417d86e6e08b9a8d471a5ff10ed2dbe83599990753ec6dec"}
EJECUTABLES = (".githooks/", ".bowser/costo.py", ".bowser/verificar.py")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def skill_rel(nombre: str) -> str:
    return f".opencode/skills/{nombre}/SKILL.md"


def leer_skills(archivo: Path) -> list[str]:
    if not archivo.exists():
        return []
    return [l.strip() for l in archivo.read_text(encoding="utf-8").splitlines() if l.strip() and not l.strip().startswith("#")]


# Señales para sugerir skills del catálogo (solo se sugieren; las decide la persona en .bowser/skills).
SENALES = {
    "go": ["go.mod", "*/go.mod"],
    "react": ["package.json", "*/package.json"],
    "php": ["*.php", "*/*.php", "*/*/*.php"],
    "postgres": ["docker-compose.yml", "compose.yaml", "*/migrations/*.sql"],
    "mysql": ["*.sql", "*/*.sql", "*/*/*.sql"],
    "web": ["*.html", "*/*.html", "*/*/*.html"],
}


def sugerir_skills(destino: Path) -> list[str]:
    sugeridas = []
    for nombre, patrones in SENALES.items():
        archivos = [f for pat in patrones for f in destino.glob(pat) if "node_modules" not in f.parts and "vendor" not in f.parts]
        if not archivos:
            continue
        if nombre == "react" and not any('"react"' in f.read_text(encoding="utf-8", errors="replace") for f in archivos[:5]):
            continue
        if nombre in ("postgres", "mysql"):
            motor = "postgres" if nombre == "postgres" else "mysql"
            texto = " ".join(f.read_text(encoding="utf-8", errors="replace")[:20000].lower() for f in archivos[:10])
            if motor not in texto and not (motor == "mysql" and "engine=innodb" in texto):
                continue
        sugeridas.append(nombre)
    return sugeridas


def version() -> str:
    return (KIT / "VERSION").read_text(encoding="utf-8").strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Instala o actualiza bowser-ai-lite en un proyecto.")
    ap.add_argument("proyecto", type=Path)
    ap.add_argument("--verificar", action="store_true", help="no escribe nada; dice qué cambiaría")
    ap.add_argument("--forzar", action="store_true", help="reemplaza los archivos del kit editados en el proyecto")
    ap.add_argument("--skills", help="skills de tecnología a usar, separadas por coma (se agregan a .bowser/skills)")
    a = ap.parse_args()

    destino = a.proyecto.resolve()
    if not destino.is_dir():
        print(f"✗ No existe la carpeta {destino}", file=sys.stderr)
        return 1
    if destino == KIT or KIT in destino.parents:
        print("✗ El proyecto no puede estar dentro de la carpeta del kit.", file=sys.stderr)
        return 1

    ruta_manifiesto = destino / MANIFIESTO
    anterior = json.loads(ruta_manifiesto.read_text(encoding="utf-8")) if ruta_manifiesto.exists() else {}
    hashes_previos: dict = anterior.get("archivos", {})
    escribir = not a.verificar
    cambios, avisos, manifiesto = [], [], {}

    # Skills de tecnología: las que nombra .bowser/skills del proyecto, más las de --skills.
    archivo_skills = destino / ".bowser/skills"
    skills = leer_skills(archivo_skills) if archivo_skills.exists() else []
    pedidas = [n.strip() for n in (a.skills or "").split(",") if n.strip()]
    disponibles = sorted(d.name for d in CATALOGO.iterdir() if (d / "SKILL.md").exists())
    skills_nuevas = [n for n in pedidas if n not in skills and n in disponibles]
    for n in [n for n in skills + pedidas if n not in disponibles]:
        avisos.append(f"La skill «{n}» no está en el catálogo (hay: {', '.join(disponibles)}).")
    skills = [n for n in skills if n in disponibles] + skills_nuevas

    gestionados = [(rel, fuente(rel)) for rel in DEL_KIT] + [(skill_rel(n), CATALOGO / n / "SKILL.md") for n in skills]
    for rel, origen in gestionados:
        dst = destino / rel
        nuevo = sha(origen)
        if dst.exists():
            actual = sha(dst)
            if actual == nuevo:
                manifiesto[rel] = nuevo
                continue
            editado = rel in hashes_previos and actual != hashes_previos[rel]
            ajeno = rel not in hashes_previos and actual != nuevo
            if (editado or ajeno) and not a.forzar:
                if nuevo == hashes_previos.get(rel):
                    avisos.append(f"{rel}: el proyecto tiene su propia versión; se respeta (el kit no trae cambios en él).")
                else:
                    avisos.append(f"{rel}: el proyecto tiene su propia versión y el kit trae cambios en él; no se tocó.\n"
                                  f"    Para verlos: diff -u {rel} {origen}\n"
                                  "    Pasa a mano lo que sirva. --forzar reemplaza tu versión (queda en .bowser/respaldo/) "
                                  "y tendrás que volver a aplicar tus cambios.")
                manifiesto[rel] = hashes_previos.get(rel, actual)
                continue
            if escribir and (editado or ajeno):
                respaldo = destino / ".bowser/respaldo" / rel
                respaldo.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, respaldo)
                avisos.append(f"{rel}: se reemplazó tu versión; quedó en .bowser/respaldo/{rel}. "
                              f"Compárala (diff -u .bowser/respaldo/{rel} {rel}) y vuelve a aplicar lo que era del proyecto.")
            cambios.append(f"actualizado  {rel}")
        else:
            cambios.append(f"nuevo        {rel}")
        if escribir:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origen, dst)
            if rel.startswith(EJECUTABLES):
                dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        manifiesto[rel] = nuevo


    # Lo que el kit instaló antes y ya no instala (skills que el proyecto dejó de nombrar, comandos renombrados):
    # se retira si nadie lo editó.
    for rel in [r for r in hashes_previos if r not in manifiesto]:
        dst = destino / rel
        if not dst.exists():
            continue
        if sha(dst) != hashes_previos[rel]:
            motivo = "ya no está en .bowser/skills" if rel.startswith(".opencode/skills/") else "el kit ya no lo usa"
            avisos.append(f"{rel}: {motivo}, pero fue editado; no se borró.")
            continue
        cambios.append(f"retirado     {rel}")
        if escribir:
            dst.unlink()
            try:
                dst.parent.rmdir()
            except OSError:
                pass

    for rel in SEMILLAS:
        origen, dst = fuente(rel), destino / rel
        if dst.exists():
            continue
        cambios.append(f"semilla      {rel}")
        if escribir:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origen, dst)

    if skills_nuevas:
        cambios.append(f"agregado     {', '.join(skills_nuevas)} a .bowser/skills")
        if escribir:
            base = archivo_skills.read_text(encoding="utf-8") if archivo_skills.exists() else (PLANTILLA / ".bowser/skills").read_text(encoding="utf-8")
            archivo_skills.parent.mkdir(parents=True, exist_ok=True)
            archivo_skills.write_text(base.rstrip("\n") + "\n" + "\n".join(skills_nuevas) + "\n", encoding="utf-8")
    sugeridas = [n for n in sugerir_skills(destino) if n not in skills]
    if sugeridas:
        avisos.append("Por los archivos del proyecto, quizá le sirvan estas skills: " + ", ".join(sugeridas)
                      + f". Para instalarlas: --skills {','.join(sugeridas)} (o agrégalas a .bowser/skills).")

    # AGENTS.md del kit anterior (bowser-spec-kit-ai): se deja la plantilla al lado para no perder lo que tenga.
    agents = destino / "AGENTS.md"
    if agents.exists() and "semilla      AGENTS.md" not in cambios:
        texto = agents.read_text(encoding="utf-8", errors="replace")
        if "**orquestador" in texto or "equipo/orquestador.md" in texto:
            avisos.append("AGENTS.md es el del kit anterior (el orquestador): se dejó la plantilla nueva en AGENTS.lite.md. "
                          "Pasa a ella lo que sirva y reemplaza AGENTS.md (ver https://github.com/orestesmedina/bowser-spec-ai-lite/blob/main/docs/02-instalar.md#en-un-proyecto-con-el-kit-anterior).")
            if escribir:
                shutil.copyfile(PLANTILLA / "AGENTS.md", destino / "AGENTS.lite.md")

    # El Makefile del proyecto incluye bowser.mk (el de la semilla ya lo trae).
    makefile = destino / "Makefile"
    if makefile.exists() and "semilla      Makefile" not in cambios:
        normalizado = makefile.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(normalizado).hexdigest() in MAKEFILES_VIEJOS:
            cambios.append("actualizado  Makefile (era la plantilla sin tocar: test y lint ya no bloquean el push sin definir)")
            if escribir:
                shutil.copyfile(fuente("Makefile"), makefile)
    if makefile.exists():
        texto = makefile.read_text(encoding="utf-8")
        if INCLUDE not in texto:
            cambios.append("agregado     '-include bowser.mk' al Makefile")
            if escribir:
                makefile.write_text(texto.rstrip("\n") + f"\n\n# bowser-ai-lite\n{INCLUDE}\n", encoding="utf-8")

    # .gitignore: que .env nunca se suba.
    gi = destino / ".gitignore"
    lineas = gi.read_text(encoding="utf-8").splitlines() if gi.exists() else []
    faltan = [l for l in GITIGNORE if l not in lineas]
    if faltan and set(faltan) != {GITIGNORE[0]}:
        cambios.append("agregado     reglas de secretos a .gitignore")
        if escribir:
            gi.write_text("\n".join(lineas + ([""] if lineas else []) + faltan) + "\n", encoding="utf-8")

    # Avisos sobre lo que ya había.
    oc = destino / "opencode.json"
    if oc.exists():
        try:
            agente = json.loads(oc.read_text(encoding="utf-8")).get("default_agent")
        except ValueError:
            agente = None
            avisos.append("opencode.json no es JSON válido: revísalo.")
        if agente and agente != "constructor":
            avisos.append(f"opencode.json abre el agente «{agente}» por defecto. Para usar el kit, cambia default_agent a \"constructor\".")
    if (destino / ".kit-manifest.json").exists():
        avisos.append("Este proyecto tiene instalado bowser-spec-kit-ai (el kit anterior). Conviven mal: "
                      "sigue los pasos de https://github.com/orestesmedina/bowser-spec-ai-lite/blob/main/docs/02-instalar.md#en-un-proyecto-con-el-kit-anterior")

    if escribir:
        ruta_manifiesto.parent.mkdir(parents=True, exist_ok=True)
        ruta_manifiesto.write_text(json.dumps({"kit": "bowser-ai-lite", "version": version(), "archivos": manifiesto},
                                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if (destino / ".git").exists():
            subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=destino, check=False)
        else:
            avisos.append("El proyecto no es un repositorio de git: los controles se activan con 'make hooks' después de 'git init'.")

    titulo = "Se haría esto" if a.verificar else f"bowser-ai-lite {version()} instalado en {destino}"
    print(titulo + ":")
    for c in cambios or ["(nada que cambiar)"]:
        print("  " + c)
    for av in avisos:
        print("⚠ " + av)
    if not a.verificar and any(c.startswith("semilla      AGENTS.md") for c in cambios):
        print("\nSiguiente paso: completa AGENTS.md y el Makefile (run, test, lint) con los datos del proyecto,\no en OpenCode: /bowser-discover (proyecto existente) o /bowser-idea (proyecto nuevo). Guía: https://github.com/orestesmedina/bowser-spec-ai-lite/blob/main/docs/README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
