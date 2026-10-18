# 2. Instalar

[← Inicio](README.md)

- [Requisitos](#requisitos)
- [Una vez por máquina](#una-vez-por-máquina)
- [En un proyecto nuevo](#en-un-proyecto-nuevo)
- [En un proyecto existente](#en-un-proyecto-existente)
- [En un proyecto con el kit anterior](#en-un-proyecto-con-el-kit-anterior)
- [La primera vez en OpenCode](#la-primera-vez-en-opencode)
- [Actualizar](#actualizar)

## Requisitos

- **Linux, macOS o Windows con WSL** (Ubuntu). En Windows, todo (git, Python, make y OpenCode) se instala y se corre dentro de WSL.
- **Git**, **Python 3.9 o más nuevo** y **make**.
- **[OpenCode](https://opencode.ai)**. Los agentes vienen configurados con modelos de OpenCode Go; si usas otro proveedor, cambia el campo `model` de cada agente (ver [Agentes](06-agentes.md#modelos)).
- Opcional: **gitleaks**, para que cada commit busque secretos con más detalle.

## Una vez por máquina

```bash
curl -fsSL https://raw.githubusercontent.com/orestesmedina/bowser-spec-ai-lite/main/install.sh | bash
```

Deja el kit en `~/.bowser-ai-lite`, en la última versión publicada, y el comando `bowser` en `~/.local/bin`. Si esa carpeta no está en tu `PATH`, el instalador te dice qué línea agregar a `~/.bashrc` o `~/.zshrc`.

| Para… | Usa |
|---|---|
| Instalar una versión concreta | `curl -fsSL …/install.sh \| bash -s -- v0.11.0` |
| Dejar el kit en otra carpeta | `BOWSER_HOME=/otra/ruta` antes de `bash` |
| Dejar el comando en otra carpeta | `BOWSER_BIN=/otra/ruta` |
| Instalar desde otro repositorio (una copia tuya) | `BOWSER_REPO=https://…` |

Comprueba con `bowser version`.

## En un proyecto nuevo

```bash
mkdir mi-proyecto && cd mi-proyecto && git init -b main
bowser init
opencode
```

En OpenCode escribe `/bowser-idea` y tu idea en una o dos frases:

```
/bowser-idea una app para que los talleres mecánicos agenden citas y avisen al cliente cuando el auto está listo
```

Te entrevista (como máximo tres rondas de cinco preguntas, cada una con su recomendación), escribe requerimientos, arquitectura, decisiones y roadmap, y te pide aprobarlos. No escribe código. Al final te dice dos cosas:

1. Qué skills instalar para la tecnología elegida: `bowser init --skills go,react,postgres`.
2. Cómo empezar: `/bowser-feature #1 del roadmap: base mínima`, en una sesión nueva. Esa primera funcionalidad deja el proyecto corriendo con `make run`, con una prueba que pasa y con `AGENTS.md` y el `Makefile` completos.

Detalle en [Comandos: /bowser-idea](05-comandos.md#bowser-idea).

## En un proyecto existente

```bash
cd /ruta/al/proyecto
bowser init --verificar                  # qué haría, sin escribir nada
bowser init --skills php,mysql           # instala, con las skills de sus tecnologías
```

Si no pones `--skills`, el instalador mira el proyecto (`go.mod`, `package.json`, `composer.json`…) y te sugiere las que parecen servirle. El instalador nunca reemplaza un archivo tuyo: si ya tienes `AGENTS.md`, `Makefile` u `opencode.json`, los deja (al `Makefile` solo le agrega la línea `-include bowser.mk`).

Luego, en OpenCode:

```
/bowser-discover
```

Hace ingeniería inversa del proyecto en cinco pasadas (inventario, módulos, datos, convenciones y deuda, y una prueba de entendimiento) y deja la memoria lista para trabajar. No cambia el código del producto. Detalle en [Comandos: /bowser-discover](05-comandos.md#bowser-discover).

Si prefieres hacerlo a mano o por partes, esto es lo mínimo antes de la primera funcionalidad:

1. **`AGENTS.md`**: qué es el proyecto, cómo se corre, su estructura y las reglas que no salen del código. Menos de ~100 líneas.
2. **`Makefile`**: los comandos `run`, `test` y `lint` reales. `check` es lo que debe pasar antes de entregar; lo corren el hook antes de cada push y el CI, así que **hasta que los definas, ni el push ni el CI pasan**. Si el CI necesita preparar algo (dependencias, una base de datos), agrega el objetivo `ci-setup`.
3. **`.bowser/inmutables`**: los archivos que no se tocan una vez en git, por ejemplo `backend/migrations/*.sql`. Revisa también `.bowser/verificacion` (ver [Controles](08-controles.md#bowserverificacion)).
4. **`docs/producto/requerimientos.md`**: empieza con visión, roles y glosario. Los `RF` de lo que ya existe se agregan al tocarlo.
5. **`docs/memoria/`**: empieza por `trampas.md` y `convenciones.md`. El resto se llena con `/bowser-close` en cada funcionalidad.
6. `git add -A && git commit -m "chore: instala bowser-ai-lite"`.

## En un proyecto con el kit anterior

`bowser-spec-kit-ai` y este kit no conviven: los dos traen `AGENTS.md`, `Makefile`, hooks y agentes de OpenCode. El instalador lo detecta y avisa. Hazlo en una rama, o mejor en una copia del proyecto.

**Antes de borrar, guarda lo que vale:**

| Del kit anterior | Pasa a |
|---|---|
| `equipo/perfil.json` → los comandos de cada verbo (`probar`, `revisar`, `formato`…) | Los comandos `test`, `lint` y `check` del `Makefile` |
| `equipo/perfil.json` → `inmutables` | `.bowser/inmutables` |
| `.agents/skills/convenciones-de-*/SKILL.md` | `docs/memoria/convenciones.md` (y su sección de deuda a `deuda.md`) |
| `equipo/reglas.md` | "Reglas que no salen del código" en `AGENTS.md` (lo que ya dice `.bowser/principios.md` no se repite) |
| `catalogo` del perfil (`go-backend`, `react-frontend`, `postgres-db`…) | `--skills go,react,postgres` al instalar |
| `proyecto.mk` | Se queda; inclúyelo desde el `Makefile` nuevo (`-include proyecto.mk`) |
| `specs/`, `docs/producto/roadmap.md` | Se quedan como historia; el roadmap se pasa al formato nuevo |

```bash
mkdir -p ~/kit-anterior && cp -r equipo .agents/skills/convenciones-de-* proyecto.mk ~/kit-anterior/ 2>/dev/null
```

**Quitar el kit anterior:**

```bash
# Los archivos que instaló (están en su manifiesto: incluye AGENTS.md, Makefile, scripts/ y .githooks/)
jq -r '.archivos | keys[]' .kit-manifest.json | xargs git rm -q --ignore-unmatch
# Lo que generaba y el submódulo
git rm -rq --ignore-unmatch CLAUDE.md opencode.json .claude .codex .opencode/agents .kit-manifest.json \
  equipo .agents/skills/bowser-* .agents/skills/convenciones-de-* .opencode/commands/bowser-*
git submodule deinit -f .bowser-spec-kit-ai && git rm -q .bowser-spec-kit-ai && rm -rf .git/modules/.bowser-spec-kit-ai
git config --unset core.hooksPath
```

Los comandos de Spec Kit (`.opencode/commands/speckit.*`, `.specify/`) se pueden quedar.

Después instala este kit como en un [proyecto existente](#en-un-proyecto-existente), pasa ahí lo que guardaste y haz un solo commit: `chore: cambia bowser-spec-kit-ai por bowser-ai-lite`.

## La primera vez en OpenCode

Abre OpenCode **en la carpeta del proyecto** (`cd proyecto && opencode`). Comprueba:

- [ ] El agente activo es `constructor`. Si no, revisa `default_agent` en `opencode.json`.
- [ ] Los modelos existen: `opencode models opencode-go` muestra los que piden `.opencode/agents/*.md` (campo `model`).
- [ ] Al escribir `/bowser` aparecen los nueve comandos.
- [ ] Puedes mencionar `@revisor` y `@explorador`.
- [ ] El agente corre pruebas sin pedir permiso, pero **pregunta** antes de `git push`.
- [ ] `git commit --allow-empty -m "hola"` falla (el mensaje no sigue Conventional Commits): los hooks están activos. Si no falla, corre `make hooks`.

Si falta un comando, cierra OpenCode del todo y vuelve a abrirlo: solo lee los comandos y agentes al arrancar. Ver [Problemas frecuentes](12-problemas.md#no-aparece-un-comando).

## Actualizar

```bash
bowser update --verificar   # qué cambiaría, sin tocar nada
bowser update               # baja la última versión del kit y actualiza este proyecto
```

O, dentro de OpenCode, `/bowser-update`, que hace lo mismo y además el commit. Muestra el CHANGELOG entre tu versión y la nueva, y respeta los archivos del kit que editaste: no los toca y, si el kit trae cambios en uno de ellos, te dice cómo verlos (`diff -u …`) para que los pases a mano. `--forzar` los reemplaza y deja tu versión en `.bowser/respaldo/`, pero **borra lo que habías cambiado**: úsalo solo si después vas a volver a aplicarlo. Después, **cierra OpenCode y vuelve a abrirlo**.

| Opción de `bowser update` | Para… |
|---|---|
| `--verificar` | Ver qué cambiaría sin tocar nada |
| `--version v0.10.0` | Ir a una versión concreta (también sirve para volver atrás) |
| `--solo-kit` | Actualizar el kit de la máquina, no el proyecto |
| `--forzar` | Reemplazar también los archivos del kit que editaste. Tu versión queda en `.bowser/respaldo/` y tienes que volver a aplicar tus cambios |

Siguiente: [3. Elegir el comando](03-elegir-el-comando.md)
