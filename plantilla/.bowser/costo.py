#!/usr/bin/env python3
"""bowser-ai-lite · Tokens y costo equivalente de la rama actual, leídos de las sesiones de OpenCode.

Uso: python3 .bowser/costo.py [--todo] [--desde AAAA-MM-DD] [--json]

- Por defecto cuenta las sesiones de este proyecto desde que se creó la rama actual (o desde su primer commit).
- --todo cuenta todas las sesiones del proyecto. --desde fija el inicio a mano.
- El costo es el que calcula OpenCode a precio de API ("equivalente"). Con OpenCode Go, el gasto real es el
  porcentaje que muestra su consola. Los tokens sí son reales y son la medida que conviene comparar.

Formatos soportados (verificados en bowser-spec-kit-ai con OpenCode 1.18 y 2.0.22):
  1.x: `opencode export <id>`; mensajes {info: {role, agent, providerID, modelID, tokens, cost, time}, parts}.
  2.x: `opencode session export <id>`; mensajes planos {type, agent, model: {id, providerID}, tokens, cost, time}.
Solo biblioteca estándar de Python 3.9+.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


class Fallo(Exception):
    pass


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def opencode(*args: str) -> str:
    # A un archivo temporal: OpenCode 2.x corta los JSON grandes cuando escribe a una tubería.
    try:
        with tempfile.TemporaryFile("w+", encoding="utf-8") as salida:
            r = subprocess.run(["opencode", *args], stdout=salida, stderr=subprocess.PIPE, text=True,
                               cwd=RAIZ, timeout=180)
            salida.seek(0)
            texto = salida.read()
    except FileNotFoundError:
        raise Fallo("no se encontró el programa 'opencode' en el PATH")
    except subprocess.TimeoutExpired:
        raise Fallo(f"'opencode {args[0]}' tardó demasiado")
    if r.returncode != 0:
        raise Fallo(f"'opencode {' '.join(args[:2])}' falló: {r.stderr.strip()[:200]}")
    return texto


_MAYOR: int | None = None


def version_mayor() -> int:
    global _MAYOR
    if _MAYOR is None:
        try:
            m = re.search(r"(\d+)\.\d+", opencode("--version"))
        except Fallo:
            m = None
        _MAYOR = int(m.group(1)) if m else 2
    return _MAYOR


def json_de(texto: str):
    inicio = min([i for i in (texto.find("{"), texto.find("[")) if i >= 0], default=-1)
    if inicio < 0:
        raise Fallo("OpenCode no devolvió JSON")
    return json.loads(texto[inicio:])


def sesiones_del_proyecto() -> list[dict]:
    orden = ("session", "list", "--format", "json", "-n", "1000")
    datos = json_de(opencode(*orden) or "[]")
    if not datos and version_mayor() >= 2:
        # En 2.x el servicio en segundo plano a veces devuelve la lista vacía; leyendo directo sí aparecen.
        datos = json_de(opencode(*orden, "--standalone") or "[]")
    raiz = str(RAIZ)
    return [s for s in datos if str(Path(s.get("directory", "") or "/").resolve()).startswith(raiz)]


def exportar(sid: str) -> dict:
    orden = ("session", "export") if version_mayor() >= 2 else ("export",)
    return json_de(opencode(*orden, sid))


def hijas(export: dict) -> list[str]:
    """Sesiones de subagentes lanzadas desde esta sesión."""
    ids: list[str] = []

    def agregar(sid) -> None:
        if sid and sid not in ids:
            ids.append(sid)

    for m in export.get("messages", []):
        for p in m.get("parts", []) or []:                    # 1.x
            if p.get("type") == "tool" and p.get("tool") == "task":
                agregar(((p.get("state") or {}).get("metadata") or {}).get("sessionId"))
        for c in m.get("content") or []:                      # 2.x
            if isinstance(c, dict) and c.get("type") == "tool" and c.get("name") in ("subagent", "task"):
                meta = (c.get("state") or {}).get("metadata") or {}
                agregar(meta.get("sessionID") or meta.get("sessionId"))
        meta = m.get("metadata") or {}
        if m.get("type") == "synthetic" and meta.get("source") == "subagent":
            agregar(meta.get("childID"))
    return ids


def respuestas(export: dict) -> list[dict]:
    resultado = []
    for m in export.get("messages", []):
        info = m.get("info") or m
        if (info.get("role") or info.get("type")) != "assistant":
            continue
        t = info.get("tokens") or {}
        cache = t.get("cache") or {}
        tokens = {"entrada": t.get("input", 0) or 0, "salida": (t.get("output", 0) or 0) + (t.get("reasoning", 0) or 0),
                  "cache": (cache.get("read", 0) or 0) + (cache.get("write", 0) or 0)}
        if not any(tokens.values()):
            continue
        modelo = info.get("model") if isinstance(info.get("model"), dict) else {}
        resultado.append({
            "ms": (info.get("time") or {}).get("created", 0) or 0,
            "agente": info.get("agent") or info.get("mode") or "?",
            "modelo": info.get("modelID") or modelo.get("id") or "?",
            "tokens": tokens,
            "costo": float(info.get("cost") or 0),
        })
    return resultado


def inicio_de_rama() -> tuple[int, str]:
    rama = git("rev-parse", "--abbrev-ref", "HEAD")
    reflog = git("reflog", "show", "--date=unix", "--format=%gd", rama) if rama else ""
    lineas = [l for l in reflog.splitlines() if "@{" in l]
    if lineas:
        try:
            return int(lineas[-1].split("@{")[1].rstrip("}")) * 1000, rama
        except ValueError:
            pass
    base = git("merge-base", "HEAD", "main") or git("merge-base", "HEAD", "master")
    primeros = git("log", "--reverse", "--format=%ct", f"{base}..HEAD").splitlines() if base else []
    if primeros:
        return int(primeros[0]) * 1000, rama
    return 0, rama


def fmt_tokens(n: float) -> str:
    for limite, sufijo in ((1e9, " G"), (1e6, " M"), (1e3, " k")):
        if n >= limite:
            return f"{n / limite:.1f}{sufijo}"
    return str(int(n))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--todo", action="store_true", help="todas las sesiones del proyecto")
    ap.add_argument("--desde", help="contar desde esta fecha (AAAA-MM-DD)")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    a = ap.parse_args()

    if a.todo:
        desde, titulo = 0, "todo el proyecto"
    elif a.desde:
        desde = int(dt.datetime.fromisoformat(a.desde).timestamp() * 1000)
        titulo = f"desde {a.desde}"
    else:
        desde, rama = inicio_de_rama()
        titulo = f"rama {rama or '?'}"
        if rama in ("main", "master"):
            print("⚠ Estás en la rama principal: se cuentan todas las sesiones. Usa --desde o cambia a la rama de la funcionalidad.",
                  file=sys.stderr)
            desde = 0

    try:
        sesiones = [s for s in sesiones_del_proyecto() if (s.get("updated") or s.get("created") or 0) >= desde]
        vistas, pendientes, filas = set(), [s["id"] for s in sesiones if s.get("id")], []
        while pendientes:
            sid = pendientes.pop()
            if sid in vistas:
                continue
            vistas.add(sid)
            exp = exportar(sid)
            filas += [r for r in respuestas(exp) if r["ms"] >= desde]
            pendientes += hijas(exp)
    except Fallo as e:
        print(f"✗ No se pudo leer el consumo de OpenCode: {e}", file=sys.stderr)
        return 1

    grupos: dict[tuple[str, str], dict] = {}
    for r in filas:
        g = grupos.setdefault((r["agente"], r["modelo"]), {"respuestas": 0, "entrada": 0, "salida": 0, "cache": 0, "costo": 0.0})
        g["respuestas"] += 1
        for k in ("entrada", "salida", "cache"):
            g[k] += r["tokens"][k]
        g["costo"] += r["costo"]
    total = {k: sum(g[k] for g in grupos.values()) for k in ("respuestas", "entrada", "salida", "cache", "costo")}
    total["tokens"] = total["entrada"] + total["salida"] + total["cache"]

    if a.json:
        print(json.dumps({"alcance": titulo, "sesiones": len(vistas), "total": total,
                          "por_agente": [{"agente": ag, "modelo": mo, **g} for (ag, mo), g in sorted(grupos.items())]},
                         ensure_ascii=False, indent=2))
        return 0

    print(f"Costo de IA · {titulo} · {len(vistas)} sesiones (incluye subagentes)\n")
    if not filas:
        print("  Todavía no hay consumo registrado.")
        return 0
    print(f"  {'Agente':<14} {'Modelo':<26} {'Resp.':>6} {'Entrada':>9} {'Salida':>9} {'Caché':>9} {'Costo eq.':>10}")
    for (ag, mo), g in sorted(grupos.items(), key=lambda x: -(x[1]["entrada"] + x[1]["salida"] + x[1]["cache"])):
        print(f"  {ag[:14]:<14} {mo[:26]:<26} {g['respuestas']:>6} {fmt_tokens(g['entrada']):>9} "
              f"{fmt_tokens(g['salida']):>9} {fmt_tokens(g['cache']):>9} {'$' + format(g['costo'], '.2f'):>10}")
    print(f"\n  Total: {fmt_tokens(total['tokens'])} tokens · ${total['costo']:.2f} equivalente · {total['respuestas']} respuestas")
    print("  (Con OpenCode Go el gasto real es el % de su consola; los tokens son la medida para comparar.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
