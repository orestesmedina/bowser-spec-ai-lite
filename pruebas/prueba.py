#!/usr/bin/env python3
"""Pruebas de bowser-ai-lite: instalan el kit en proyectos temporales y comprueban lo que promete.

Uso: python3 pruebas/prueba.py      (necesita git y bash; no necesita OpenCode: se simula)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
PLANTILLA = KIT / "plantilla"
FALLOS: list[str] = []


def caso(nombre: str, condicion: bool, detalle: str = "") -> None:
    print(("  ✓ " if condicion else "  ✗ ") + nombre + ("" if condicion else f"  ({detalle})"))
    if not condicion:
        FALLOS.append(nombre)


def sh(cmd: list[str], cwd: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env={**os.environ, **(env or {})})


def proyecto(base: Path, nombre: str, git: bool = True) -> Path:
    p = base / nombre
    p.mkdir()
    if git:
        sh(["git", "init", "-q", "-b", "main"], p)
        sh(["git", "config", "user.email", "prueba@example.com"], p)
        sh(["git", "config", "user.name", "Prueba"], p)
    return p


def instalar(p: Path, *extra: str) -> subprocess.CompletedProcess:
    return sh([sys.executable, str(KIT / "instalar.py"), str(p), *extra], KIT)


def commit(p: Path, mensaje: str) -> subprocess.CompletedProcess:
    return sh(["git", "commit", "-q", "-m", mensaje], p)


def prueba_instalacion(base: Path) -> None:
    print("Instalación")
    p = proyecto(base, "nuevo")
    r = instalar(p)
    caso("instala sin error", r.returncode == 0, r.stderr)
    for rel in ["AGENTS.md", "Makefile", "bowser.mk", "opencode.json", ".opencode/agents/constructor.md",
                ".opencode/commands/bowser-feature.md", "docs/memoria/decisiones.md", ".bowser/kit.json", ".bowser/costo.py",
                ".github/workflows/bowser.yml"]:
        caso(f"existe {rel}", (p / rel).exists())
    caso("los hooks son ejecutables", os.access(p / ".githooks/pre-commit", os.X_OK) and os.access(p / ".githooks/commit-msg", os.X_OK))
    caso("activa los hooks en git", sh(["git", "config", "core.hooksPath"], p).stdout.strip() == ".githooks")
    caso(".gitignore protege .env", ".env" in (p / ".gitignore").read_text().splitlines())
    oc = json.loads((p / "opencode.json").read_text())
    caso("OpenCode abre el agente constructor", oc.get("default_agent") == "constructor")

    r = instalar(p)
    caso("reinstalar no cambia nada", "(nada que cambiar)" in r.stdout, r.stdout)

    # Un archivo del kit editado en el proyecto se respeta.
    rev = p / ".opencode/agents/revisor.md"
    rev.write_text(rev.read_text() + "\nRegla propia.\n")
    r = instalar(p)
    caso("respeta un archivo del kit editado", "Regla propia" in rev.read_text() and "revisor.md" in r.stdout, r.stdout)
    r = instalar(p, "--forzar")
    caso("--forzar lo reemplaza", "Regla propia" not in rev.read_text())
    caso("--forzar deja respaldo", "Regla propia" in (p / ".bowser/respaldo/.opencode/agents/revisor.md").read_text())
    caso("--forzar avisa que hay que volver a aplicar lo propio", "vuelve a aplicar" in r.stdout, r.stdout)

    # Un archivo editado que el kit cambia: no se toca, y el aviso dice cómo ver los cambios del kit.
    kit_json = p / ".bowser/kit.json"
    datos = json.loads(kit_json.read_text())
    datos["archivos"][".opencode/agents/revisor.md"] = "0" * 64  # el kit instaló otra versión antes
    kit_json.write_text(json.dumps(datos))
    rev.write_text(rev.read_text() + "\nRegla propia.\n")
    r = instalar(p)
    caso("si el kit cambia un archivo editado, lo respeta y muestra cómo ver el diff",
         "Regla propia" in rev.read_text() and "kit trae cambios" in r.stdout and "diff -u .opencode/agents/revisor.md" in r.stdout, r.stdout)
    instalar(p, "--forzar")

    # Las semillas son del proyecto: no se reemplazan.
    (p / "docs/memoria/trampas.md").write_text("mía\n")
    instalar(p)
    caso("no reemplaza una semilla", (p / "docs/memoria/trampas.md").read_text() == "mía\n")

    # Comandos que el kit renombró (0.7 -> 0.8): el viejo se retira si nadie lo editó.
    import hashlib
    kit = json.loads((p / ".bowser/kit.json").read_text())
    for viejo, texto in [("feature", "viejo\n"), ("cerrar", "viejo\n")]:
        (p / f".opencode/commands/{viejo}.md").write_text(texto)
        kit["archivos"][f".opencode/commands/{viejo}.md"] = hashlib.sha256(texto.encode()).hexdigest()
    (p / ".bowser/kit.json").write_text(json.dumps(kit))
    (p / ".opencode/commands/cerrar.md").write_text("viejo y editado\n")
    r = instalar(p)
    caso("retira un comando con nombre viejo", not (p / ".opencode/commands/feature.md").exists() and "retirado" in r.stdout, r.stdout)
    caso("no borra un comando viejo editado", (p / ".opencode/commands/cerrar.md").exists() and "ya no lo usa" in r.stdout, r.stdout)
    (p / ".opencode/commands/cerrar.md").unlink()
    caso("los comandos usan el prefijo bowser-", sorted(x.name for x in (p / ".opencode/commands").iterdir()) ==
         ["bowser-close.md", "bowser-cost.md", "bowser-discover.md", "bowser-feature.md", "bowser-idea.md", "bowser-resume.md", "bowser-review.md", "bowser-roadmap.md", "bowser-update.md"])

    # --verificar no escribe.
    q = proyecto(base, "verificar")
    r = instalar(q, "--verificar")
    caso("--verificar no escribe nada", not any(q.iterdir()) or [x.name for x in q.iterdir()] == [".git"], str(list(q.iterdir())))
    caso("--verificar dice qué haría", "nuevo" in r.stdout and "AGENTS.md" in r.stdout)

    # Proyecto que ya tiene Makefile y el AGENTS.md del kit anterior.
    v = proyecto(base, "existente")
    (v / "Makefile").write_text("test:\n\tgo test ./...\n")
    (v / "AGENTS.md").write_text("Eres el **orquestador / jefe de proyecto**. Lee equipo/orquestador.md\n")
    (v / ".kit-manifest.json").write_text("{}")
    r = instalar(v)
    mk = (v / "Makefile").read_text()
    caso("agrega el include al Makefile existente", "-include bowser.mk" in mk and "go test" in mk, mk)
    caso("no pisa el AGENTS.md anterior", "orquestador" in (v / "AGENTS.md").read_text())
    caso("deja la plantilla en AGENTS.lite.md", (v / "AGENTS.lite.md").exists())
    caso("avisa del kit anterior", "kit anterior" in r.stdout, r.stdout)
    r = instalar(v)
    caso("el include no se duplica", (v / "Makefile").read_text().count("-include bowser.mk") == 1)


def prueba_skills(base: Path) -> None:
    print("Principios y skills de tecnología")
    p = proyecto(base, "skills")
    (p / "go.mod").write_text("module ejemplo\n\ngo 1.27\n")
    r = instalar(p)
    caso("instala los principios del kit", (p / ".bowser/principios.md").exists())
    caso("sin pedirlas no instala skills", not (p / ".opencode/skills").exists())
    caso("sugiere la skill de Go por go.mod", "go" in r.stdout and "--skills" in r.stdout, r.stdout)
    r = instalar(p, "--skills", "go,react,cobol")
    caso("instala las skills pedidas", (p / ".opencode/skills/go/SKILL.md").exists() and (p / ".opencode/skills/react/SKILL.md").exists())
    caso("las anota en .bowser/skills", {"go", "react"} <= set((p / ".bowser/skills").read_text().split()))
    caso("avisa de una skill que no existe", "cobol" in r.stdout and not (p / ".opencode/skills/cobol").exists(), r.stdout)
    caso("no anota la que no existe", "cobol" not in (p / ".bowser/skills").read_text())
    caso("reinstalar no cambia nada", "(nada que cambiar)" in instalar(p).stdout)
    txt = (p / ".bowser/skills").read_text().replace("react\n", "")
    (p / ".bowser/skills").write_text(txt)
    r = instalar(p)
    caso("retira la skill que se quitó de la lista", not (p / ".opencode/skills/react").exists() and "retirado" in r.stdout, r.stdout)
    go = p / ".opencode/skills/go/SKILL.md"
    go.write_text(go.read_text() + "\nPropio.\n")
    (p / ".bowser/skills").write_text(txt.replace("go\n", ""))
    r = instalar(p)
    caso("no borra una skill editada", go.exists() and "editado" in r.stdout, r.stdout)
    caso("el constructor lee los principios", ".bowser/principios.md" in (p / ".opencode/agents/constructor.md").read_text())


def prueba_documentacion(base: Path) -> None:
    print("Estándar de documentación")
    p = proyecto(base, "docs")
    instalar(p)
    caso("instala el estándar de documentación", (p / ".bowser/documentacion.md").exists())
    caso("siembra los requerimientos", (p / "docs/producto/requerimientos.md").exists())
    req = (p / "docs/producto/requerimientos.md").read_text()
    caso("los requerimientos traen RF y criterios", "RF-01" in req and "Dado" in req and "Preguntas abiertas" in req)
    for rel in ["AGENTS.md", ".opencode/agents/constructor.md", ".opencode/commands/bowser-close.md"]:
        caso(f"{rel} remite al estándar", ".bowser/documentacion.md" in (p / rel).read_text())
    caso("/bowser-feature pide los RF del cambio", "RF-NN" in (p / ".opencode/commands/bowser-feature.md").read_text())
    caso("el revisor revisa los criterios de aceptación", "criterio de aceptación" in (p / ".opencode/agents/revisor.md").read_text())
    tipos = ("flowchart", "sequenceDiagram", "erDiagram", "stateDiagram-v2")
    bloques = []
    for md in sorted(PLANTILLA.rglob("*.md")):
        partes = md.read_text().split("```")
        caso(f"cercas de código cerradas en {md.relative_to(PLANTILLA)}", len(partes) % 2 == 1)
        bloques += [(md.name, b[len("mermaid"):].strip()) for b in partes[1::2] if b.startswith("mermaid")]
    caso("las plantillas traen diagramas", len(bloques) >= 4, str(len(bloques)))
    for nombre, b in bloques:
        caso(f"diagrama válido en {nombre} ({b.split()[0]})", b.split()[0] in tipos and "<" not in b, b[:60])


def prueba_hooks(base: Path) -> None:
    print("Controles de git")
    p = proyecto(base, "hooks")
    instalar(p)
    sh(["git", "add", "-A"], p)
    caso("acepta Conventional Commits", commit(p, "chore: instala bowser-ai-lite").returncode == 0)
    (p / "a.txt").write_text("a")
    sh(["git", "add", "a.txt"], p)
    r = commit(p, "cambios varios")
    caso("rechaza un mensaje sin formato", r.returncode != 0 and "Conventional" in r.stderr, r.stderr)
    commit(p, "feat: archivo a")

    (p / ".env").write_text("CLAVE=secreta\n")
    sh(["git", "add", "-f", ".env"], p)
    r = commit(p, "chore: configura")
    caso("bloquea subir .env", r.returncode != 0 and ".env" in r.stderr, r.stderr)
    sh(["git", "rm", "-q", "--cached", ".env"], p)
    (p / ".env.example").write_text("CLAVE=\n")
    sh(["git", "add", ".env.example"], p)
    caso("permite .env.example", commit(p, "docs: variables de entorno").returncode == 0)

    (p / "migrations").mkdir()
    (p / "migrations/001_inicio.sql").write_text("CREATE TABLE a (id int);\n")
    with open(p / ".bowser/inmutables", "a") as f:
        f.write("migrations/*.sql\n")
    sh(["git", "add", "-A"], p)
    caso("un archivo inmutable nuevo se puede agregar", commit(p, "feat: primera migración").returncode == 0)
    (p / "migrations/001_inicio.sql").write_text("CREATE TABLE a (id bigint);\n")
    sh(["git", "add", "-A"], p)
    r = commit(p, "fix: cambia migración")
    caso("bloquea modificar un inmutable versionado", r.returncode != 0 and "inmutable" in r.stderr, r.stderr)
    sh(["git", "checkout", "-q", "--", "."], p)
    sh(["git", "reset", "-q"], p)
    sh(["git", "checkout", "-q", "--", "."], p)
    sh(["git", "rm", "-q", "migrations/001_inicio.sql"], p)
    r = commit(p, "chore: borra migración")
    caso("bloquea borrar un inmutable versionado", r.returncode != 0 and "inmutable" in r.stderr, r.stderr)
    sh(["git", "reset", "-q", "HEAD", "--", "migrations/001_inicio.sql"], p)
    sh(["git", "checkout", "-q", "--", "migrations/001_inicio.sql"], p)
    sh(["git", "mv", "migrations/001_inicio.sql", "migrations/001_otro.sql"], p)
    r = commit(p, "chore: renombra migración")
    caso("bloquea renombrar un inmutable versionado", r.returncode != 0 and "001_inicio.sql" in r.stderr, r.stderr)


OPENCODE_FALSO = r'''#!/usr/bin/env python3
import json, os, sys
v = os.environ.get("OC_VERSION", "2")
args = sys.argv[1:]
ahora = int(os.environ["OC_AHORA"])
def resp(agente, modelo, n, costo, cache=0):
    if v == "1":
        return {"info": {"role": "assistant", "agent": agente, "providerID": "opencode-go", "modelID": modelo,
                         "time": {"created": ahora + n}, "cost": costo,
                         "tokens": {"input": 1000, "output": 200, "reasoning": 50, "cache": {"read": cache, "write": 0}}}, "parts": []}
    return {"type": "assistant", "agent": agente, "model": {"id": modelo, "providerID": "opencode-go"},
            "time": {"created": ahora + n}, "cost": costo,
            "tokens": {"input": 1000, "output": 200, "reasoning": 50, "cache": {"read": cache, "write": 0}}, "content": []}
if args[:1] == ["--version"]:
    print("opencode v2.0.30" if v == "2" else "1.18.3"); sys.exit()
if args[:2] == ["session", "list"]:
    print(json.dumps([{"id": "raiz", "updated": ahora + 10, "created": ahora, "directory": os.getcwd()},
                      {"id": "vieja", "updated": 1000, "created": 900, "directory": os.getcwd()},
                      {"id": "otra", "updated": ahora, "created": ahora, "directory": "/otro/proyecto"}])); sys.exit()
sid = args[-1]
if sid == "raiz":
    ms = [resp("constructor", "deepseek-v4.1-flash", 1, 0.5, cache=5000), resp("constructor", "deepseek-v4.1-flash", 2, 0.25)]
    if v == "1":
        ms.append({"info": {"role": "assistant", "time": {"created": ahora + 3}}, "parts": [
            {"type": "tool", "tool": "task", "state": {"metadata": {"sessionId": "hija"}}}]})
    else:
        ms.append({"type": "synthetic", "metadata": {"source": "subagent", "childID": "hija"}, "time": {"created": ahora + 3}})
elif sid == "hija":
    ms = [resp("constructor" if os.environ.get("OC_SIN_REVISOR") else "revisor", "mimo-v2.6-pro", 4, 0.1)]
else:
    ms = [resp("constructor", "deepseek-v4.1-flash", -10**12, 9.0)]
print("Exportando…")
print(json.dumps({"info": {"id": sid}, "messages": ms}))
'''


def prueba_costo(base: Path) -> None:
    print("Costo (OpenCode simulado)")
    p = proyecto(base, "costo")
    instalar(p)
    sh(["git", "add", "-A"], p)
    commit(p, "chore: instala")
    sh(["git", "checkout", "-q", "-b", "feat/algo"], p)
    bin_dir = base / "bin"
    bin_dir.mkdir(exist_ok=True)
    falso = bin_dir / "opencode"
    falso.write_text(OPENCODE_FALSO)
    falso.chmod(0o755)
    ahora = int(time.time() * 1000) + 60_000
    for v in ("2", "1"):
        env = {"PATH": f"{bin_dir}:{os.environ['PATH']}", "OC_VERSION": v, "OC_AHORA": str(ahora)}
        r = sh([sys.executable, ".bowser/costo.py", "--json"], p, env)
        if r.returncode != 0:
            caso(f"OpenCode {v}.x: se ejecuta", False, r.stderr)
            continue
        d = json.loads(r.stdout)
        caso(f"OpenCode {v}.x: suma la sesión y su subagente", d["sesiones"] == 2, d)
        caso(f"OpenCode {v}.x: ignora otras carpetas y sesiones viejas", abs(d["total"]["costo"] - 0.85) < 1e-9, d["total"])
        agentes = {x["agente"]: x for x in d["por_agente"]}
        caso(f"OpenCode {v}.x: separa por agente y modelo", set(agentes) == {"constructor", "revisor"} and agentes["revisor"]["modelo"] == "mimo-v2.6-pro", agentes)
        caso(f"OpenCode {v}.x: cuenta razonamiento como salida y la caché", agentes["constructor"]["salida"] == 500 and agentes["constructor"]["cache"] == 5000, agentes["constructor"])
    env = {"PATH": f"{bin_dir}:{os.environ['PATH']}", "OC_VERSION": "2", "OC_AHORA": str(ahora)}
    r = sh(["make", "-s", "cost"], p, env)
    caso("make cost muestra la tabla", r.returncode == 0 and "Total:" in r.stdout, r.stdout + r.stderr)
    r = sh([sys.executable, ".bowser/costo.py"], p, {"PATH": "/usr/bin:/bin"})
    caso("sin OpenCode falla con un mensaje claro", r.returncode != 0 and "opencode" in r.stderr, r.stderr)


def prueba_verificacion(base: Path) -> None:
    print("Verificación de la rama (make verify, pre-push y CI)")
    p = proyecto(base, "verificar-rama")
    instalar(p)
    (p / "Makefile").write_text("-include bowser.mk\n\ncheck:\n\t@test ! -f FALLA\n")
    sh(["git", "add", "-A"], p)
    commit(p, "chore: instala")
    sh(["git", "checkout", "-q", "-b", "feat/descuentos"], p)
    bin_dir = base / "bin-verificar"
    bin_dir.mkdir()
    (bin_dir / "opencode").write_text(OPENCODE_FALSO)
    (bin_dir / "opencode").chmod(0o755)
    ahora = int(time.time() * 1000) + 60_000
    env = {"PATH": f"{bin_dir}:{os.environ['PATH']}", "OC_VERSION": "2", "OC_AHORA": str(ahora)}

    def verificar(*extra: str, **mas: str) -> subprocess.CompletedProcess:
        return sh([sys.executable, ".bowser/verificar.py", *extra], p, {**env, **mas})

    (p / "descuentos.go").write_text("package main\n")
    sh(["git", "add", "-A"], p)
    commit(p, "feat: descuentos")
    r = verificar()
    caso("falla si cambia código sin pruebas", r.returncode != 0 and "sin cambiar pruebas" in r.stdout, r.stdout)
    (p / "descuentos_test.go").write_text("package main\n")
    sh(["git", "add", "-A"], p)
    commit(p, "test: descuentos")
    r = verificar()
    caso("pasa con código, pruebas y revisión", r.returncode == 0 and "revisor revisó" in r.stdout, r.stdout + r.stderr)
    r = verificar(OC_SIN_REVISOR="1")
    caso("falla si el revisor no revisó la rama", r.returncode != 0 and "revisor no revisó" in r.stdout, r.stdout)
    r = verificar(PATH="/usr/bin:/bin")
    caso("sin OpenCode no da la revisión por buena", r.returncode != 0 and "no se pudo comprobar la revisión" in r.stdout, r.stdout)
    (p / "FALLA").write_text("")
    r = verificar()
    caso("falla si make check falla", r.returncode != 0 and "make check falla" in r.stdout, r.stdout)
    r = sh(["make", "-s", "verify"], p, env)
    caso("make verify corre la verificación", r.returncode != 0 and "Verificación de la rama" in r.stdout, r.stdout)
    (p / "FALLA").unlink()
    futuro = str(int(time.time()) + 3600)
    (p / "descuentos.go").write_text("package main\n\n// ajuste\n")
    sh(["git", "add", "-A"], p)
    sh(["git", "commit", "-q", "-m", "fix: ajuste"], p, {"GIT_COMMITTER_DATE": f"{futuro} +0000", "GIT_AUTHOR_DATE": f"{futuro} +0000"})
    r = verificar()
    caso("avisa si hubo código después de la revisión", r.returncode == 0 and "después de la última revisión" in r.stdout, r.stdout)

    # Tamaño: archivos riesgosos exigen un plan grande commiteado antes.
    sh(["git", "checkout", "-q", "main"], p)
    sh(["git", "checkout", "-q", "-b", "feat/roles"], p)
    (p / "migrations").mkdir()
    (p / "migrations/002_roles.sql").write_text("CREATE TABLE roles (id int);\n")
    sh(["git", "add", "-A"], p)
    commit(p, "feat: tabla de roles")
    r = verificar("--sin-check")
    caso("falla si toca algo riesgoso sin plan", r.returncode != 0 and "no tiene plan" in r.stdout, r.stdout)
    sh(["git", "reset", "-q", "--hard", "main"], p)
    (p / "docs/cambios").mkdir(parents=True)
    (p / "docs/cambios/roles.md").write_text("**Tamaño:** normal\n")
    sh(["git", "add", "-A"], p)
    commit(p, "docs: plan de roles")
    (p / "migrations").mkdir()
    (p / "migrations/002_roles.sql").write_text("CREATE TABLE roles (id int);\n")
    sh(["git", "add", "-A"], p)
    commit(p, "feat: tabla de roles")
    r = verificar("--sin-check")
    caso("falla si el plan no es de tamaño grande", r.returncode != 0 and "Tamaño: grande" in r.stdout, r.stdout)
    sh(["git", "reset", "-q", "--hard", "main"], p)
    (p / "docs/cambios").mkdir(parents=True)
    (p / "migrations").mkdir()
    (p / "docs/cambios/roles.md").write_text("**Tamaño:** grande\n")
    (p / "migrations/002_roles.sql").write_text("CREATE TABLE roles (id int);\n")
    sh(["git", "add", "-A"], p)
    commit(p, "feat: roles con su plan")
    r = verificar("--sin-check")
    caso("falla si el plan llega junto con el código", r.returncode != 0 and "va primero" in r.stdout, r.stdout)
    sh(["git", "reset", "-q", "--hard", "main"], p)
    (p / "docs/cambios").mkdir(parents=True)
    (p / "docs/cambios/roles.md").write_text("**Tamaño:** grande\n")
    sh(["git", "add", "-A"], p)
    commit(p, "docs: plan de roles")
    (p / "migrations").mkdir()
    (p / "migrations/002_roles.sql").write_text("CREATE TABLE roles (id int);\n")
    sh(["git", "add", "-A"], p)
    commit(p, "feat: tabla de roles\n\nSin-pruebas: solo crea la tabla; la prueba llega con el servicio")
    r = verificar("--sin-check")
    caso("pasa con plan grande previo", r.returncode == 0 and "plan grande previo" in r.stdout, r.stdout)
    caso("acepta Sin-pruebas con motivo y lo muestra", "con motivo: solo crea la tabla" in r.stdout, r.stdout)
    caso("avisa si la migración no actualizó base-de-datos.md", "no se actualizó docs/memoria/base-de-datos.md" in r.stdout, r.stdout)
    caso("avisa de una carpeta de código nueva sin arquitectura.md", "carpetas de código nuevas (migrations)" in r.stdout, r.stdout)
    caso("los avisos de memoria no bloquean", r.returncode == 0)
    with open(p / "docs/memoria/base-de-datos.md", "a") as fh:
        fh.write("\n| roles | Roles de usuario | id | — |\n")
    (p / "docs/memoria/arquitectura.md").write_text((p / "docs/memoria/arquitectura.md").read_text() + "\nmigrations/\n")
    r = verificar("--sin-check")
    caso("cuenta la memoria aún sin commitear", "la memoria acompaña los cambios" in r.stdout, r.stdout)
    sh(["git", "checkout", "-q", "--", "docs/memoria"], p)
    r = verificar("--ci", "--base", "main", PATH="/usr/bin:/bin")
    caso("--ci no necesita OpenCode ni make check", r.returncode == 0 and "revis" not in r.stdout and "make check" not in r.stdout, r.stdout + r.stderr)

    # pre-push: lo que no pasa make check no sale.
    remoto = base / "remoto.git"
    sh(["git", "init", "-q", "--bare", str(remoto)], base)
    sh(["git", "remote", "add", "origin", str(remoto)], p)
    (p / "FALLA").write_text("")
    r = sh(["git", "push", "-q", "origin", "feat/roles"], p)
    caso("pre-push bloquea si make check falla", r.returncode != 0 and "make check falla" in r.stderr, r.stderr)
    (p / "FALLA").unlink()
    r = sh(["git", "push", "-q", "origin", "feat/roles"], p)
    caso("pre-push deja subir si make check pasa", r.returncode == 0, r.stderr)
    (p / "Makefile").write_text("-include bowser.mk\n")
    r = sh(["git", "push", "-q", "origin", "HEAD:otra"], p)
    caso("pre-push exige un objetivo check", r.returncode != 0 and "'check'" in r.stderr, r.stderr)
    ci = (p / ".github/workflows/bowser.yml").read_text()
    idea = (p / ".opencode/commands/bowser-idea.md").read_text()
    caso("instala /bowser-idea", "agent: constructor" in idea and "$ARGUMENTS" in idea)
    caso("/bowser-idea no escribe código y pide aprobación", "no escribes código" in idea and "No sigas sin esa aprobación" in idea)
    for doc in ["docs/producto/requerimientos.md", "docs/memoria/arquitectura.md", "docs/memoria/decisiones.md", "docs/producto/roadmap.md", "AGENTS.md"]:
        caso(f"/bowser-idea escribe {doc} y existe su plantilla", doc in idea and (p / doc).exists())
    caso("/bowser-idea pone la base mínima como #1", "base mínima" in idea and "#1" in idea)
    rm = (p / ".opencode/commands/bowser-roadmap.md").read_text()
    caso("instala /bowser-roadmap", "agent: constructor" in rm and "$ARGUMENTS" in rm)
    caso("/bowser-roadmap informa sin tocar nada y solo replanea si se pide", "sin modificar nada" in rm and "terminas aquí" in rm)
    for doc in ["docs/producto/roadmap.md", "docs/producto/requerimientos.md", "docs/memoria/producto.md", "docs/memoria/deuda.md", "docs/cambios/"]:
        caso(f"/bowser-roadmap lee {doc}", doc in rm)
    dc = (p / ".opencode/commands/bowser-discover.md").read_text()
    caso("instala /bowser-discover", "agent: constructor" in dc and "$ARGUMENTS" in dc)
    caso("/bowser-discover no cambia cómo funciona el sistema", "sin cambiar cómo funciona" in dc)
    caso("/bowser-discover lee el esquema real y no lee .env", "se **lee, no se recuerda**" in dc and "no leas `.env`" in dc)
    caso("/bowser-discover reparte los módulos al explorador", "@explorador" in dc)
    caso("/bowser-discover pide confirmar un flujo a la persona", "Explica un flujo clave" in dc)
    caso("/bowser-discover lleva su avance para /bowser-resume", "docs/cambios/descubrimiento.md" in dc and "/bowser-resume" in dc)
    for doc in ["AGENTS.md", "docs/memoria/arquitectura.md", "docs/memoria/producto.md", "docs/producto/requerimientos.md",
                "docs/memoria/base-de-datos.md", "docs/memoria/convenciones.md", "docs/memoria/deuda.md", "docs/memoria/decisiones.md",
                "docs/memoria/trampas.md", "docs/memoria/modulos.md", ".bowser/inmutables", ".bowser/verificacion"]:
        caso(f"/bowser-discover escribe {doc} y existe su plantilla", doc.split("/")[-1] in dc and (p / doc).exists())
    est = (p / ".bowser/estandares.md").read_text()
    caso("instala las preguntas de estándares", "Idioma del código" in est and "Nombre de cada capa" in est and "El código que ya existe" in est)
    caso("las preguntas de estándares valen para cualquier lenguaje", "cualquier lenguaje" in est)
    caso("/bowser-discover pregunta cómo lo quiere la persona", "## 6. Cómo lo quieres de aquí en adelante" in dc and ".bowser/estandares.md" in dc)
    caso("/bowser-discover escribe las convenciones como heredadas y luego decididas", "(heredada)" in dc and "(decidida, D-NN)" in dc)
    caso("/bowser-discover no reescribe una memoria que ya existe", "no la reescribas" in dc)
    conv = (p / "docs/memoria/convenciones.md").read_text()
    caso("la plantilla de convenciones distingue decidida y heredada", "(decidida" in conv and "(heredada)" in conv)
    caso("AGENTS.md dice cuándo leer modulos.md", "`modulos.md`" in (p / "AGENTS.md").read_text())
    caso("el revisor revisa las fronteras de modulos.md", "`modulos.md`" in (p / ".opencode/agents/revisor.md").read_text())
    caso("el plan de /bowser-feature dice qué diseño toca", "Diseño que toca" in (p / ".opencode/commands/bowser-feature.md").read_text())
    caso("/bowser-close mantiene modulos.md", "`modulos.md`" in (p / ".opencode/commands/bowser-close.md").read_text())
    faltan = [d.name for d in sorted((KIT / "catalogo").iterdir()) if "**decidida**" not in (d / "SKILL.md").read_text(encoding="utf-8")]
    caso("cada skill cede ante una convención decidida", not faltan, str(faltan))
    caso("/bowser-feature escribe pruebas de caracterización", "pruebas de caracterización" in (p / ".opencode/commands/bowser-feature.md").read_text())
    caso("instala /bowser-resume", "Estado" in (p / ".opencode/commands/bowser-resume.md").read_text())
    caso("el plan de /bowser-feature lleva su Estado", "/bowser-resume" in (p / ".opencode/commands/bowser-feature.md").read_text())
    caso("el CI corre make check y la verificación de la rama", "run: make check" in ci and "verificar.py --ci" in ci)


def prueba_workflow(base: Path) -> None:
    print("Workflow del proyecto")
    wf = (PLANTILLA / "github/bowser.yml").read_text(encoding="utf-8")
    caso("el workflow pide solo lectura, con permiso para listar los commits del pull request (gitleaks)",
         "permissions:\n  contents: read\n  pull-requests: read\n" in wf and "write" not in wf)

    # El paso de versiones, tal como corre en el CI, en proyectos con y sin .bowser/versiones.
    lineas = wf.split("        id: versiones\n        run: |\n", 1)[1].splitlines()
    script = "\n".join(l[10:] for l in lineas[:next(i for i, l in enumerate(lineas) if not l.startswith("          "))])

    def versiones(archivos: dict[str, str]) -> dict[str, str]:
        d = Path(tempfile.mkdtemp(dir=base))
        sh(["git", "init", "-q"], d)
        for rel, texto in archivos.items():
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            (d / rel).write_text(texto)
        sh(["git", "add", "-A"], d)
        salida = d / "salida"
        sh(["bash", "-c", script], d, {**os.environ, "GITHUB_OUTPUT": str(salida)})
        return dict(l.split("=", 1) for l in salida.read_text().splitlines())

    v = versiones({".bowser/versiones": "go=\nphp=8.4   # la de producción\nnode=22\n", "tracker/go.mod": "module x\n\ngo 1.27.1\n"})
    caso("el CI usa las versiones de .bowser/versiones y la de go.mod si no hay", v == {"go": "1.27.1", "php": "8.4", "node": "22"}, v)
    v = versiones({".bowser/versiones": "go=1.26\n", "go.mod": "module x\n\ngo 1.27\n"})
    caso("la versión de .bowser/versiones manda sobre go.mod", v.get("go") == "1.26", v)
    v = versiones({"README.md": "hola\n"})
    caso("sin versiones, el CI usa las más nuevas", v == {"go": "stable", "php": "latest", "node": "lts/*"}, v)


def prueba_wiki(base: Path) -> None:
    print("Documentación del kit (docs/)")
    import re
    sys.path.insert(0, str(KIT))
    import instalar as kit

    def ancla(titulo: str) -> str:
        return re.sub(r"[^\w\- ]", "", titulo.strip().lower()).replace(" ", "-")

    paginas = sorted((KIT / "docs").glob("*.md")) + [KIT / "README.md", KIT / "GUIA.md"]
    anclas = {}
    for f in paginas:
        sin_codigo = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        anclas[f.resolve()] = (sin_codigo, {ancla(h) for h in re.findall(r"^#+ (.+)$", sin_codigo, re.M)})
    rotos = []
    for f, (texto, _) in anclas.items():
        for enlace in re.findall(r"\]\(([^)\s]+)\)", texto):
            if enlace.startswith(("http://", "https://")):
                continue
            ruta, _, a = enlace.partition("#")
            destino = (f.parent / ruta).resolve() if ruta else f
            if not destino.exists() or (a and destino in anclas and a not in anclas[destino][1]):
                rotos.append(f"{f.name}: {enlace}")
    caso("los enlaces de la documentación llevan a una página y sección que existen", not rotos, "; ".join(rotos))
    comandos = (KIT / "docs/05-comandos.md").read_text(encoding="utf-8")
    inicio = (KIT / "docs/README.md").read_text(encoding="utf-8")
    faltan = [Path(r).stem for r in kit.DEL_KIT if r.startswith(".opencode/commands/")
              and (f"## /{Path(r).stem}" not in comandos or f"`/{Path(r).stem}`" not in inicio)]
    caso("cada comando tiene su sección en Comandos y su línea en el inicio", not faltan, faltan)


def prueba_distribucion(base: Path) -> None:
    print("Distribución: install.sh, bowser init y bowser update")
    import shutil
    origen = base / "origen"
    shutil.copytree(KIT, origen, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    for c in (["init", "-q", "-b", "main"], ["config", "user.email", "kit@example.com"], ["config", "user.name", "Kit"]):
        sh(["git", *c], origen)
    actual = (KIT / "VERSION").read_text().strip()

    def publicar(version: str, nota: str) -> None:
        sh(["git", "add", "-A"], origen)
        sh(["git", "commit", "-q", "-m", f"chore: versión {version}"], origen)
        sh(["git", "tag", f"v{version}"], origen)

    publicar(actual, "")
    (origen / "VERSION").write_text("9.9.9\n")
    log = (origen / "CHANGELOG.md").read_text()
    (origen / "CHANGELOG.md").write_text(log.replace("## [", "## [9.9.9] - 2099-01-01\n\n- Cambio de prueba.\n\n## [", 1))
    with open(origen / "plantilla/.bowser/principios.md", "a") as fh:
        fh.write("\n17. Regla nueva de prueba.\n")
    publicar("9.9.9", "")

    casa = base / "casa"
    env = {"BOWSER_REPO": str(origen), "BOWSER_HOME": str(casa / ".bowser-ai-lite"), "BOWSER_BIN": str(casa / "bin")}
    r = sh(["bash", str(KIT / "install.sh"), f"v{actual}"], base, env)
    bowser = casa / "bin/bowser"
    caso("install.sh instala la versión pedida", r.returncode == 0 and f"bowser-ai-lite {actual} instalado" in r.stdout, r.stdout + r.stderr)
    caso("deja el comando bowser", bowser.exists() and os.access(bowser, os.X_OK))
    caso("avisa si la carpeta del comando no está en el PATH", "no está en tu PATH" in r.stdout, r.stdout)

    p = proyecto(base, "con-bowser")
    r = sh([str(bowser), "init", "--skills", "go"], p)
    caso("bowser init instala el kit en la carpeta actual", r.returncode == 0 and json.loads((p / ".bowser/kit.json").read_text())["version"] == actual, r.stdout + r.stderr)
    caso("bowser init pasa las skills", (p / ".opencode/skills/go/SKILL.md").exists())
    sh(["git", "add", "-A"], p)
    commit(p, "chore: instala bowser-ai-lite")
    r = sh([str(bowser), "version"], p)
    caso("bowser version muestra kit y proyecto", f"Kit: bowser-ai-lite {actual}" in r.stdout and f"Proyecto: {actual}" in r.stdout, r.stdout)

    r = sh([str(bowser), "update", "--verificar"], p)
    caso("update --verificar muestra la versión nueva y sus cambios", f"{actual} → 9.9.9" in r.stdout and "Cambio de prueba" in r.stdout, r.stdout + r.stderr)
    caso("update --verificar dice qué cambiaría en el proyecto", "principios.md" in r.stdout, r.stdout)
    caso("update --verificar no cambia nada", (casa / ".bowser-ai-lite/VERSION").read_text().strip() == actual
         and json.loads((p / ".bowser/kit.json").read_text())["version"] == actual and "17." not in (p / ".bowser/principios.md").read_text())

    r = sh([str(bowser), "update"], p)
    caso("bowser update actualiza el kit", (casa / ".bowser-ai-lite/VERSION").read_text().strip() == "9.9.9", r.stdout + r.stderr)
    caso("bowser update actualiza el proyecto", json.loads((p / ".bowser/kit.json").read_text())["version"] == "9.9.9"
         and "Regla nueva de prueba" in (p / ".bowser/principios.md").read_text(), r.stdout + r.stderr)
    caso("recuerda reiniciar OpenCode", "Cierra OpenCode" in r.stdout)
    caso("respeta las skills del proyecto al actualizar", (p / ".opencode/skills/go/SKILL.md").exists())
    r = sh([str(bowser), "update"], p)
    caso("sin versión nueva, lo dice", "ya es la última versión" in r.stdout, r.stdout)

    (casa / ".bowser-ai-lite/README.md").write_text("cambio local\n")
    (origen / "VERSION").write_text("9.9.10\n")
    publicar("9.9.10", "")
    r = sh([str(bowser), "update"], p)
    caso("no pisa cambios locales en la copia del kit", r.returncode != 0 and "cambios locales" in r.stderr
         and (casa / ".bowser-ai-lite/VERSION").read_text().strip() == "9.9.9", r.stdout + r.stderr)

    otra = base / "casa2"
    r = sh(["bash", str(KIT / "install.sh")], base, {**env, "BOWSER_HOME": str(otra / "kit"), "BOWSER_BIN": str(otra / "bin")})
    caso("sin versión pedida instala la última publicada", "bowser-ai-lite 9.9.10 instalado" in r.stdout, r.stdout + r.stderr)
    up = (p / ".opencode/commands/bowser-update.md").read_text()
    caso("/bowser-update verifica, pregunta y recuerda reiniciar", "bowser update --verificar" in up and "Solo con un sí" in up and "cierre OpenCode" in up)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="bowser-lite-") as tmp:
        base = Path(tmp)
        prueba_instalacion(base)
        prueba_skills(base)
        prueba_documentacion(base)
        prueba_hooks(base)
        prueba_costo(base)
        prueba_verificacion(base)
        prueba_distribucion(base)
        prueba_workflow(base)
        prueba_wiki(base)
    print()
    if FALLOS:
        print(f"✗ {len(FALLOS)} pruebas fallaron: " + "; ".join(FALLOS))
        return 1
    print("✓ Todas las pruebas pasaron.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
