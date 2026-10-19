# 11. Archivos que instala

[← Inicio](README.md)

Los archivos que el kit deja en tu proyecto son de dos tipos:

- **Del kit**: se reemplazan al actualizar. Si editas uno, el instalador lo detecta (guarda su huella en `.bowser/kit.json`), **no lo toca** y avisa. Si el kit trae cambios en un archivo que editaste, el aviso te dice cómo verlos para pasarlos a mano. `--forzar` lo reemplaza y deja tu versión en `.bowser/respaldo/`; lo que habías cambiado se pierde hasta que lo vuelvas a aplicar.
- **Del proyecto**: se copian solo si no existen, como punto de partida. Desde ahí son tuyos y el kit nunca los vuelve a tocar.

Por eso lo que el proyecto necesita ajustar va en sus propios archivos, no en los del kit: las reglas en `AGENTS.md`, las versiones del CI en `.bowser/versiones` y lo que el CI prepara en `make ci-setup`.

Si una versión nueva del kit deja de usar un archivo suyo (por ejemplo, un comando que cambió de nombre), el instalador lo borra, salvo que lo hayas editado: en ese caso lo deja y avisa.

## Del kit

| Archivo | Qué es |
|---|---|
| `.opencode/agents/constructor.md`, `revisor.md`, `explorador.md` | Los [agentes](06-agentes.md) |
| `.opencode/commands/bowser-*.md` | Los nueve [comandos](05-comandos.md) |
| `.opencode/skills/<nombre>/SKILL.md` | Las [skills](09-skills.md) que elegiste |
| `.bowser/principios.md` | Reglas de seguridad, calidad y datos para cualquier proyecto |
| `.bowser/documentacion.md` | El [formato](07-memoria.md#el-formato) de requisitos, diagramas y decisiones |
| `.bowser/estandares.md` | Las preguntas de estándares (idioma, nombres, capas, errores, carpetas) que `/bowser-idea` y `/bowser-discover` le hacen a la persona |
| `.bowser/verificar.py` | `make verify` |
| `.bowser/costo.py` | `make cost` |
| `.githooks/pre-commit`, `commit-msg`, `pre-push` | Los [hooks de git](08-controles.md#hooks-de-git) |
| `.github/workflows/bowser.yml` | El [CI](08-controles.md#el-ci) del proyecto |
| `bowser.mk` | Los objetivos `verify`, `cost` y `hooks`, que el `Makefile` incluye |

## Del proyecto

| Archivo | Qué es |
|---|---|
| `AGENTS.md` | Los hechos de este proyecto: qué es, cómo se corre, estructura, reglas propias, tecnologías y cuándo leer cada archivo de la memoria. Menos de ~100 líneas |
| `Makefile` | `run`, `test`, `lint`, `check` y opcionalmente `ci-setup`. Si ya tenías uno, solo se le agrega `-include bowser.mk` |
| `opencode.json` | Abre OpenCode con el agente `constructor` y fija el modelo para tareas chicas |
| `.bowser/verificacion` | Qué cuenta como prueba, como riesgo y como código ([detalle](08-controles.md#bowserverificacion)) |
| `.bowser/versiones` | Las versiones de Go, PHP y Node que usa el CI ([detalle](08-controles.md#el-ci)) |
| `.bowser/inmutables` | Archivos que no se modifican una vez en git |
| `.bowser/skills` | Las skills del proyecto, una por línea |
| `docs/producto/requerimientos.md`, `roadmap.md`, `historial.md` | Qué se construye, en qué orden y qué se entregó |
| `docs/memoria/*.md` | La [memoria](07-memoria.md): producto, arquitectura, módulos, base de datos, decisiones, trampas, convenciones y deuda |

## Lo que se crea al trabajar

| Archivo | Lo crea |
|---|---|
| `docs/cambios/<nombre>.md` | `/bowser-feature` (el plan de cada cambio normal o grande) y `/bowser-discover` (su avance) |
| `.bowser/kit.json` | El instalador: la versión instalada y la huella de cada archivo del kit. Se commitea; no lo edites |
| `.bowser/respaldo/` | `--forzar`: tus versiones de archivos del kit reemplazados. Está en `.gitignore` |

El instalador también agrega a `.gitignore` las reglas para que `.env` y `.env.*` (salvo `.env.example`) nunca se suban.

## Qué se commitea

Todo lo anterior, salvo `.bowser/respaldo/`. Los agentes, comandos y hooks van en git para que cualquiera que clone el proyecto trabaje igual; después de clonar, solo hace falta `make hooks`.

Siguiente: [12. Problemas frecuentes](12-problemas.md)
