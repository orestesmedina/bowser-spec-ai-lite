# Guía

- [1. Instalar en un proyecto](#1-instalar-en-un-proyecto)
- [2. Proyecto con el kit anterior](#2-proyecto-con-el-kit-anterior)
- [3. Primera vez en OpenCode: qué comprobar](#3-primera-vez-en-opencode-qué-comprobar)
- [4. La prueba de la fase 1](#4-la-prueba-de-la-fase-1)
- [5. Si se corta la sesión](#5-si-se-corta-la-sesión)
- [6. Publicar una versión del kit](#6-publicar-una-versión-del-kit)

Todo se ejecuta dentro de WSL (Ubuntu). El comando `bowser` se instala una vez por máquina:

```bash
curl -fsSL https://raw.githubusercontent.com/orestesmedina/bowser-spec-ai-lite/main/install.sh | bash
```

Mientras trabajas en el kit mismo, puedes usar tu copia sin instalar: `python3 /mnt/d/IA/bowser-ai-lite/bin/bowser init`.

## 1. Instalar en un proyecto

**Proyecto nuevo, desde una idea:**

```bash
mkdir mi-proyecto && cd mi-proyecto && git init -b main
bowser init
opencode
```

En OpenCode: `/bowser-idea <tu idea en una o dos frases>`. Te entrevista, escribe requerimientos, arquitectura, decisiones y roadmap, y te pide aprobarlos. Al final te dice qué skills instalar (`bowser init --skills …`) y con qué empezar: `/bowser-feature #1 del roadmap: base mínima`, en una sesión nueva. Los pasos de abajo (AGENTS.md, Makefile) los hace esa funcionalidad #1.

**Proyecto existente:**

```bash
cd /ruta/al/proyecto
bowser init --verificar                  # qué haría, sin escribir
bowser init --skills go,react,postgres   # las tecnologías del proyecto
```

Skills disponibles: `go`, `react`, `postgres`, `php`, `mysql`, `web`. Si no pones `--skills`, el instalador sugiere las que encuentre. `.bowser/principios.md` se instala siempre.

Luego, a mano o pidiéndoselo al agente con `/bowser-feature` (tamaño pequeño):

1. **`AGENTS.md`**: qué es el proyecto, cómo se corre, su estructura y las reglas que no salen del código. Menos de ~100 líneas.
2. **`Makefile`**: los comandos `run`, `test` y `lint` reales. `check` es lo que debe pasar antes de entregar: lo corren el hook antes de cada push y el CI, así que hasta que los definas, ni el push ni el CI pasan. Si el CI necesita preparar algo (dependencias, una base de datos), agrega el objetivo `ci-setup`.
3. **`.bowser/inmutables`**: por ejemplo `backend/migrations/*.sql`. Revisa también `.bowser/verificacion`: qué cuenta como prueba y qué es riesgoso en tu proyecto.
4. **`docs/producto/requerimientos.md`**: en un proyecto nuevo, escríbelo antes de la primera funcionalidad (visión, roles, alcance y los primeros `RF`). En uno existente, empieza solo con visión, roles y glosario; los `RF` que ya existen se agregan al tocarlos (o todos de una vez con `/bowser-discover`, cuando exista). El formato está en `.bowser/documentacion.md`.
5. **`docs/memoria/`**: no hace falta llenarla toda el primer día. Empieza por `trampas.md` y `convenciones.md`; el resto se llena con `/bowser-close` en cada funcionalidad.
6. `git add -A && git commit -m "chore: instala bowser-ai-lite"`.

## 2. Proyecto con el kit anterior

`bowser-spec-kit-ai` y este kit no conviven: los dos traen `AGENTS.md`, `Makefile`, hooks y agentes de OpenCode. Hazlo **en una copia** del proyecto (ver la sección 4) y en una rama.

**Antes de borrar, guarda lo que vale** (son del proyecto y se reaprovechan):

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

Los comandos de Spec Kit (`.opencode/commands/speckit.*`, `.specify/`) se pueden quedar: sirven para funcionalidades grandes.

**Instalar este kit** (sección 1) y pasar ahí lo que guardaste. Un solo commit: `chore: cambia bowser-spec-kit-ai por bowser-ai-lite`.

## 3. Primera vez en OpenCode: qué comprobar

Las pruebas del kit simulan OpenCode. La primera vez, en la versión real, comprueba (y anota lo que falle):

- [ ] Al abrir OpenCode en el proyecto, el agente activo es `constructor` (si no, revisa `default_agent` en `opencode.json`).
- [ ] Los modelos existen: `opencode models opencode-go` muestra `deepseek-v4.1-flash`, `mimo-v2.6-pro` y `glm-5.3-flash`.
- [ ] `/bowser-feature`, `/bowser-review`, `/bowser-close` y `/bowser-cost` aparecen al escribir `/`.
- [ ] Puedes mencionar `@revisor` y `@explorador`, y el revisor no puede editar archivos.
- [ ] El agente corre pruebas sin pedir permiso, pero **pregunta** antes de `git push`. Si pregunta por todo o no pregunta por nada, el formato de permisos por patrón de tu versión es distinto: avísame.
- [ ] `make cost` muestra la tabla de la rama.
- [ ] Después de pedir `/bowser-review`, `make verify` dice "el revisor revisó la rama". Si dice que no, el nombre del agente en las sesiones de tu versión es distinto: avísame.
- [ ] `git push` corre `make check` antes de subir.
- [ ] Cierra OpenCode a mitad de una funcionalidad, ábrelo de nuevo y escribe `/bowser-resume`: debe decir dónde quedaste sin que se lo expliques.

## 4. La prueba de la fase 1

**Objetivo:** saber si el kit nuevo hace una funcionalidad más barata, más rápida y con menos retrabajo que el anterior. La referencia: la primera funcionalidad de `simiente-santa-webside` costó **115 M tokens**, con ~110 000 tokens por respuesta del orquestador.

**Dónde:** una copia nueva y aislada de `simiente-santa-webside`. Lo aprendido el 2026-10-10 sigue valiendo:
- Sin remoto (`git remote remove origin`): un push no puede tocar el proyecto real.
- Con un `.env` de proyecto de Compose y puertos propios, y **con los contenedores reales apagados** mientras pruebas (las pruebas de integración vacían tablas y, sin `DATABASE_URL`, el código usa `localhost:5432`).

**Qué hacer:**
1. Pasar la copia al kit nuevo (sección 2) y completar `AGENTS.md`, `Makefile` y la memoria inicial.
2. Hacer **tres funcionalidades pequeñas o normales** del roadmap, cada una en **una sesión nueva** de OpenCode: `/bowser-feature …`, aprobar cuando corresponda, `/bowser-close`.
3. Una buena candidata es la deuda S1 de la funcionalidad 002: que la base de datos rechace modificar o borrar filas de `login_events` y `admin_actions`, con su prueba de integración.

**Qué anotar de cada una** (la línea de `docs/producto/historial.md` cubre casi todo):

| Dato | De dónde sale |
|---|---|
| Tokens y costo equivalente | `make cost` (lo pone `/bowser-close`) |
| Vueltas de revisión | `/bowser-close` |
| Minutos tuyos (leer, aprobar, corregir) | Tu reloj; anótalo en "Notas" |
| ¿Funcionó a la primera al probarlo tú? | Tú; en "Notas" |
| ¿El agente se equivocó por no saber algo que estaba, o debía estar, en la memoria? | Tú; en "Notas" |

Con esas tres líneas se decide qué ajustar antes de seguir con `/bowser-discover` (fase 2).

## 5. Si se corta la sesión

Un corte de internet, un reinicio o cerrar OpenCode **no pierde el trabajo**, porque nada importante vive solo en la conversación:

| Qué | Dónde queda | ¿Sobrevive? |
|---|---|---|
| Lo commiteado | git, en tu disco | Sí |
| Archivos editados y aún sin commitear | Tu disco | Sí, pero pueden estar a medias |
| Qué se pidió, qué está hecho y qué sigue | La sección **Estado** de `docs/cambios/<nombre>.md`, commiteada en cada paso | Sí |
| Lo aprendido del proyecto | `docs/memoria/` | Sí |
| La conversación | Las sesiones de OpenCode, en tu disco | Casi siempre; la respuesta que se estaba escribiendo, no |

**Para seguir:**
1. Abre OpenCode en la carpeta y busca la sesión anterior en su lista de sesiones. Si está y no es muy larga, sigue ahí.
2. Si no aparece, está muy larga o el agente parece confundido: sesión nueva y `/bowser-resume`. Te muestra qué está hecho, qué quedó sin commitear (y si pasa las pruebas) y qué seguía, y te pregunta antes de continuar.

Lo único que no protege el kit es el disco: si la máquina se daña, se pierde lo que no se subió. Sube la rama de trabajo (`git push`, que es decisión tuya) al terminar el día.

## 6. Publicar una versión del kit

En la copia de desarrollo (`D:\IA\bowser-ai-lite`), con las pruebas en verde (`python3 pruebas/prueba.py`):

1. Sube el número en `VERSION` y agrega su sección arriba en `CHANGELOG.md`.
2. `git commit -am "chore: versión X.Y.Z"`, `git tag vX.Y.Z` y `git push origin main --tags`.

`bowser update` solo ve versiones etiquetadas (`vX.Y.Z`): lo que está en `main` sin etiqueta no le llega a nadie.

