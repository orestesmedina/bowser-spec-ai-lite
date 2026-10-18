# Cambios

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado: [SemVer](https://semver.org/lang/es/).

## [0.11.1] - 2026-10-18

### Agregado
- **Documentación para cualquier persona** en [`docs/`](docs/README.md), en trece páginas: qué es y cómo piensa el kit, instalar (proyecto nuevo, existente o con el kit anterior), qué comando usar en cada situación, un día de trabajo de punta a punta, la referencia de cada comando, agentes, memoria, controles, skills, costo, archivos que instala, problemas frecuentes y cómo trabajar en el kit.
- Las pruebas del kit comprueban que los enlaces de la documentación funcionan y que cada comando tiene su página.

### Cambiado
- `GUIA.md` ahora dice dónde quedó cada sección. La prueba de la fase 1 pasó a `PLAN.md`.
- Los mensajes del instalador enlazan a la documentación y, al terminar de instalar, sugieren `/bowser-idea` o `/bowser-discover`.

## [0.11.0] - 2026-10-18

### Agregado
- **`/bowser-discover`**: ingeniería inversa de un proyecto existente en cinco pasadas, sin cambiar cómo funciona: inventario (`AGENTS.md`, piezas, trampas y skills sugeridas), módulos (resumidos por `@explorador`; arquitectura, flujos, `producto.md` y un `RF` con estado `existe` por cada comportamiento), datos (el esquema leído de migraciones o de un volcado, con `erDiagram`; nunca `.env` ni la base de producción), convenciones, deuda, decisiones "(inferida)", inmutables y `.bowser/verificacion`, y una prueba de entendimiento (levantar el sistema en local y explicar un flujo para que la persona lo confirme). Rama `docs/descubrimiento`, un commit por pasada y el avance en `docs/cambios/descubrimiento.md`, así que se puede retomar. Al final, `@revisor` comprueba al menos cinco afirmaciones contra el código.
- **Pruebas de caracterización** en `/bowser-feature`: antes de cambiar código existente sin pruebas, se escriben pruebas de cómo funciona hoy y se commitean aparte.

### Cambiado
- `/bowser-idea` y `/bowser-roadmap` mandan a `/bowser-discover` cuando el proyecto ya tiene código pero no memoria.

## [0.10.0] - 2026-10-18

### Agregado
- **Pruebas contra el OpenCode real** (`pruebas/opencode_real.py`): instala el kit en un proyecto temporal y comprueba con `opencode debug config` y `opencode debug skill` que OpenCode carga los ocho comandos con su agente, los tres agentes con su modelo y modo, los permisos (preguntar antes de `git push`, revisor sin edición) y las seis skills. No gasta tokens.
- **CI del kit** (`.github/workflows/kit.yml`): las pruebas en Linux y macOS con Python 3.9 y 3.13, las pruebas contra OpenCode real, `shellcheck` de los scripts y una corrida semanal para enterarse si una versión nueva de OpenCode deja de leer el kit.

## [0.9.0] - 2026-10-18

### Agregado
- **Instalación en un comando**: `curl -fsSL https://raw.githubusercontent.com/orestesmedina/bowser-spec-ai-lite/main/install.sh | bash`. Deja el kit en `~/.bowser-ai-lite` (en la última versión etiquetada) y el comando `bowser` en `~/.local/bin`.
- **Comando `bowser`**: `bowser init` instala el kit en un proyecto; `bowser update` baja la última versión del kit, muestra su CHANGELOG y actualiza el proyecto respetando lo editado (`--verificar` para ver sin tocar nada); `bowser version` muestra ambas versiones.
- **`/bowser-update`** en OpenCode: verifica, muestra los cambios, pregunta, actualiza y recuerda reiniciar OpenCode.
- `.gitattributes`: finales de línea LF, para que los scripts funcionen aunque el repositorio se use desde Windows.

## [0.8.0] - 2026-10-17

### Cambiado
- **Los comandos llevan el prefijo `bowser-` y nombre en inglés**, para no chocar con comandos de OpenCode o de otras herramientas. El contenido sigue en español.

  | Antes | Ahora |
  |---|---|
  | `/feature` | `/bowser-feature` |
  | `/revisar` | `/bowser-review` |
  | `/cerrar` | `/bowser-close` |
  | `/costo` | `/bowser-cost` |
  | `/retomar` | `/bowser-resume` |
  | `/idea` | `/bowser-idea` |
  | `/roadmap` | `/bowser-roadmap` |

- El instalador retira cualquier archivo que el kit instaló antes y ya no instala (como los comandos con su nombre viejo), salvo que el proyecto lo haya editado: en ese caso lo deja y avisa.

## [0.7.0] - 2026-10-17

### Agregado
- **`/roadmap`**: para retomar un proyecto sin recordar en qué iba. Primero muestra, sin tocar nada, qué es, qué está hecho, qué está en curso (con el Estado de su plan en `docs/cambios/`), qué sigue, las preguntas abiertas, la deuda de riesgo alto y las inconsistencias entre documentos. Luego pregunta si se quiere replanear (agregar, partir, reordenar o descartar funcionalidades); si no, termina sin cambiar nada. Si sí, propone la tabla nueva, espera la aprobación y actualiza roadmap, requerimientos y decisiones.

## [0.6.0] - 2026-10-17

### Agregado
- **`/idea`**: convierte una idea en un proyecto listo para construir. Entrevista en rondas cortas (con una recomendación por pregunta), escribe `requerimientos.md`, la arquitectura inicial con sus diagramas, las decisiones y el roadmap, y completa "Qué es" y "Tecnologías" en `AGENTS.md`. La funcionalidad #1 es siempre la base mínima (levanta, una prueba, `Makefile` y CI). No escribe código y no sigue sin la aprobación de la persona.

## [0.5.0] - 2026-10-17

### Agregado
- **`/retomar`**: sigue una funcionalidad a medias después de un corte, un reinicio o en una sesión nueva. Reconstruye el estado desde el disco (rama, commits, cambios sin commitear y la sección Estado del plan), comprueba con las pruebas lo que quedó sin commitear y pregunta antes de seguir.
- **Avisos de memoria vieja en `make verify`**: si la rama tocó migraciones o SQL sin actualizar `base-de-datos.md`, creó carpetas de código sin actualizar `arquitectura.md`, o cambió el Makefile o Compose sin actualizar `AGENTS.md`. Cuenta lo aún no commiteado y no bloquea. Las reglas están en la sección `[memoria]` de `.bowser/verificacion`.

### Cambiado
- El plan de `/feature` termina con una sección **Estado** (hecho, siguiente, por decidir) que el constructor actualiza y commitea en cada paso. El estado de una funcionalidad ya no vive solo en la conversación.
- `/cerrar` vuelve a correr `make verify` después de actualizar la memoria y resuelve o explica cada aviso.

## [0.4.0] - 2026-10-15

Controles contra el vibecoding: lo importante ya no depende de que el agente obedezca.

### Agregado
- **`make verify`** (`.bowser/verificar.py`): comprueba que la rama se puede cerrar. Corre `make check`; exige pruebas si cambió código (o un commit con `Sin-pruebas: <motivo>`); si tocó archivos riesgosos, exige un plan con «Tamaño: grande» commiteado antes; y comprueba en las sesiones de OpenCode que el agente `revisor` revisó la rama, avisando si hubo código después.
- **`.bowser/verificacion`** (del proyecto): qué cuenta como prueba, qué es riesgoso (migraciones, SQL, autenticación, permisos, pagos, inmutables) y qué no es código.
- **Hook `pre-push`**: no deja subir si `make check` falla o no existe.
- **CI**: el workflow corre `make check` (con Go, Node o PHP si el proyecto los usa, y `make ci-setup` si existe) y, en cada pull request, la verificación de la rama.

### Cambiado
- `/cerrar` empieza con `make verify` y no cierra si algo falla. `/feature` exige el plan commiteado antes del código, marca como grande todo lo que toque archivos riesgosos y hace obligatoria la revisión.
- El constructor y los principios prohíben aflojar los controles (`.bowser/verificacion`, hooks, CI) para que algo pase.

## [0.3.0] - 2026-10-15

### Agregado
- **`.bowser/documentacion.md`**: el estándar de documentación, igual para un proyecto nuevo y uno existente. Dice qué va en cada archivo de `docs/`, cómo se escriben los requisitos (`RF-NN` con criterios *Dado / Cuando / Entonces*, `RNF-NN` comprobables), qué diagramas Mermaid se usan y dónde (contexto, contenedores, datos, secuencia, estados) y cómo se registran las decisiones. Es del kit.
- **`docs/producto/requerimientos.md`**: plantilla con visión, usuarios y roles, alcance, requisitos funcionales y no funcionales, restricciones, preguntas abiertas y glosario. Sirve igual si se escribe desde la idea o se descubre del código.

### Cambiado
- `docs/memoria/arquitectura.md` trae diagramas de contexto, contenedores y secuencia de ejemplo, y una sección de despliegue.
- `docs/memoria/decisiones.md` usa entradas `D-NN` con contexto, decisión, lo descartado y su consecuencia.
- El roadmap tiene una columna con los requisitos que cubre cada funcionalidad.
- `/feature` liga el plan a los `RF` que cubre o agrega y, en un cambio grande, pide sus diagramas. `/cerrar` pasa esos requisitos a `existe` y lleva los diagramas a la memoria. El revisor comprueba los criterios de aceptación.

## [0.2.0] - 2026-10-15

### Agregado
- **`.bowser/principios.md`**: las reglas que valen en cualquier proyecto (seguridad, calidad, datos, personas). Es del kit: el proyecto no las puede quitar, solo agregar en `AGENTS.md`. El constructor lo lee al empezar y el revisor revisa contra él.
- **Catálogo de skills de tecnología**: `go`, `react`, `postgres`, `php`, `mysql` y `web`, traídas de `bowser-spec-kit-ai` 1.22.0 y adaptadas (convenciones y deuda en `docs/memoria/`, comandos en el `Makefile`). Se instalan en `.opencode/skills/` y OpenCode las carga solo cuando hacen falta.
- `instalar.py --skills go,react`: instala las skills pedidas y las anota en `.bowser/skills`. Si se quita una de ahí, la siguiente instalación la retira (si nadie la editó). Sin `--skills`, sugiere las que el proyecto parece usar.

### Cambiado
- Los principios de seguridad salen de la plantilla de `AGENTS.md`, que ahora remite a `.bowser/principios.md` y tiene una sección "Tecnologías".

### Límites
- Las seis skills siguen "redactadas": ninguna se usó todavía en un proyecto real con este kit.

## [0.1.0] - 2026-10-14

Primera versión, fases 0 y 1 del plan.

### Agregado
- Agentes de OpenCode: `constructor` (principal), `revisor` y `explorador`.
- Comandos: `/feature` (con tamaño pequeño, normal o grande), `/revisar`, `/cerrar` y `/costo`.
- Plantillas: `AGENTS.md`, `Makefile`, memoria del proyecto (`docs/memoria/`), roadmap e historial de entregas.
- Controles de git: secretos, Conventional Commits y archivos inmutables (`.bowser/inmutables`).
- `make cost`: tokens y costo equivalente de la rama, desde las sesiones de OpenCode 1.x y 2.x.
- `instalar.py`: instala y actualiza; respeta lo editado en el proyecto; `--verificar` y `--forzar`.
- Pruebas del kit: `python3 pruebas/prueba.py`.

### Límites
- No se probó todavía dentro de OpenCode real: las pruebas simulan OpenCode. Los permisos por patrón de `bash` en los agentes y el campo `agent` de los comandos siguen la documentación de OpenCode; hay que confirmarlos en la versión instalada.
