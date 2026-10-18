# bowser-ai-lite

Un kit pequeño para construir software con un agente de IA en **OpenCode**, con controles que no dependen de que el agente obedezca y una **memoria del proyecto** que sabe lo que el código no dice.

Es la segunda versión de [bowser-spec-kit-ai](https://github.com/orestesmedina/bowser-spec-kit-ai), rehecha a partir de su auditoría: menos agentes, menos ceremonia y más verificación.

## La idea en un minuto

- **Un agente principal (`constructor`) hace el trabajo de punta a punta:** entiende, planea, programa, prueba y entrega. Dos ayudantes: `@explorador`, que lee código y resume, y `@revisor`, que revisa al final con ojos frescos.
- **La ceremonia depende del tamaño:** un cambio pequeño va directo; uno normal lleva un plan de una página; uno grande lleva spec y plan aprobados.
- **Evidencia antes que documentos:** la persona aprueba viendo pruebas en verde y la app funcionando.
- **Memoria del proyecto en `docs/memoria/`:** decisiones, trampas, base de datos, convenciones. El agente la lee cuando la necesita y la actualiza al cerrar cada funcionalidad.
- **Documentación con formato fijo** (`.bowser/documentacion.md`): requerimientos con criterios de aceptación, diagramas en Mermaid y decisiones. El mismo formato sirve para un proyecto que nace de una idea y para uno existente que se documenta leyendo su código.
- **Principios del kit** (`.bowser/principios.md`): seguridad, calidad y datos. Valen en todo proyecto y el proyecto no los puede quitar.
- **Estándares por tecnología** como skills que se cargan solo cuando hacen falta: `go`, `react`, `postgres`, `php`, `mysql` y `web`. Cada proyecto instala solo las suyas.
- **Controles que no dependen del agente:** secretos, mensajes de commit y archivos inmutables en cada commit; `make check` antes de cada push y en el CI; y `make verify` al cerrar, que exige pruebas, un plan grande para lo riesgoso y la revisión del `@revisor` (comprobada en las sesiones de OpenCode).

## Instalar en un proyecto

Requisitos: Git, Python 3.9+, `make` y OpenCode (en Windows, todo dentro de WSL/Ubuntu).

Una vez por máquina:

```bash
curl -fsSL https://raw.githubusercontent.com/orestesmedina/bowser-spec-ai-lite/main/install.sh | bash
```

Deja el kit en `~/.bowser-ai-lite` y el comando `bowser` en `~/.local/bin`. En la carpeta de cada proyecto:

```bash
bowser init --skills go,react,postgres
```

`--skills` es opcional: el instalador mira el proyecto y sugiere las que parecen servirle. Quedan anotadas en `.bowser/skills`; para quitar una, se borra de ahí y se vuelve a instalar.

Después, en el proyecto:
1. Completa `AGENTS.md` (qué es, cómo se corre, reglas) y los comandos `run`, `test` y `lint` del `Makefile`.
2. Si el proyecto tiene archivos que no deben modificarse una vez versionados (migraciones), anótalos en `.bowser/inmutables`.
3. Revisa los modelos en `.opencode/agents/*.md` (campo `model`) y confírmalos con `opencode models opencode-go`.
4. Abre OpenCode en la carpeta: arranca con el agente `constructor`.

Para actualizar, en la carpeta del proyecto: `bowser update` (o `/bowser-update` dentro de OpenCode). Baja la última versión publicada del kit, te muestra sus cambios y actualiza el proyecto, respetando lo que editaste. `bowser update --verificar` dice qué cambiaría sin tocar nada, y `bowser version` muestra la versión del kit y la del proyecto.

## Uso diario

| Quiero… | Escribo en OpenCode |
|---|---|
| Empezar un proyecto desde una idea | `/bowser-idea una app para que los talleres agenden citas` |
| Una funcionalidad, un arreglo o un cambio | `/bowser-feature los clientes pueden exportar sus pedidos a Excel` |
| Una revisión independiente de la rama | `/bowser-review` |
| Cerrar lo terminado (memoria, historial, costo) | `/bowser-close` |
| Saber cuánto lleva gastado la rama | `/bowser-cost` o `make cost` |
| Saber si la rama se puede cerrar | `make verify` (lo corre `/bowser-close`) |
| Seguir algo a medias tras un corte o en otra sesión | `/bowser-resume` |
| Ver en qué va el proyecto, o cambiar el plan | `/bowser-roadmap` |
| Actualizar el kit en el proyecto | `/bowser-update` o `bowser update` |

## Qué instala

| Archivo | De quién es |
|---|---|
| `.opencode/agents/` (constructor, revisor, explorador), `.opencode/commands/`, `.opencode/skills/` (las elegidas), `.bowser/principios.md`, `.bowser/documentacion.md`, `.githooks/`, `.bowser/costo.py`, `.bowser/verificar.py`, `bowser.mk`, `.github/workflows/bowser.yml` | **Del kit:** se reemplazan al actualizar. Si los editas, el instalador no los toca y avisa |
| `AGENTS.md`, `Makefile`, `opencode.json`, `docs/memoria/`, `docs/producto/`, `.bowser/inmutables`, `.bowser/skills`, `.bowser/verificacion` | **Del proyecto:** se copian solo si no existen |

## Estado

Versión 0.9.0: fases 0, 1 y 3 del plan: el ciclo de una funcionalidad, la memoria, los principios, los estándares por tecnología y de documentación, los controles que no dependen del agente, `/bowser-idea` para empezar desde una idea y `/bowser-roadmap` para ver el estado y replanear. Las seis skills vienen de `bowser-spec-kit-ai` y siguen sin probarse en un proyecto real. Pendiente: `/bowser-discover` (proyectos existentes). Ver `PLAN.md` y `GUIA.md`.

## Pruebas del kit

```bash
python3 pruebas/prueba.py
```

## Licencia

[MIT](LICENSE) © Infinity Solutions AI.
