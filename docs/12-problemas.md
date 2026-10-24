# 12. Problemas frecuentes

[← Inicio](README.md)

- [En OpenCode](#en-opencode)
- [Con git](#con-git)
- [Con make verify](#con-make-verify)
- [Con el comando bowser](#con-el-comando-bowser)
- [Con el trabajo a medias](#con-el-trabajo-a-medias)

## En OpenCode

### No aparece un comando

OpenCode solo lee comandos y agentes **al arrancar**. Después de instalar o actualizar el kit, ciérralo del todo y vuelve a abrirlo en la carpeta del proyecto. **Con OpenCode 2**, antes de abrirlo corre `opencode reload`: su servicio de fondo sigue corriendo con la configuración de antes aunque cierres la ventana.

Si sigue sin aparecer:

1. Comprueba que el archivo está: `ls .opencode/commands/`.
2. Pregúntale a OpenCode qué cargó, sin abrir la interfaz:
   ```bash
   opencode debug config > /tmp/config.json && grep -o '"bowser-[a-z]*"' /tmp/config.json | sort -u
   ```
3. Si el archivo está y `debug config` lo muestra, pero la interfaz no, puede quedar un proceso de OpenCode viejo en segundo plano. Míralos con su carpeta (Linux y WSL) y cierra solo los de este proyecto, no los de otros:
   ```bash
   for p in $(pgrep -f opencode); do echo "$p $(readlink /proc/$p/cwd)"; done
   kill <el número del proceso de este proyecto>
   ```
4. Abriste OpenCode en otra carpeta: los comandos son del proyecto, así que solo aparecen si lo abres en su raíz.

### El agente no es `constructor`

`opencode.json` debe tener `"default_agent": "constructor"`. Si el proyecto ya tenía su propio `opencode.json`, el instalador no lo reemplazó y te avisó: agrega esa línea.

### Un modelo no existe

`opencode models opencode-go` muestra los disponibles. Cambia el campo `model` del agente en `.opencode/agents/` (ver [Agentes: modelos](06-agentes.md#modelos)).

### El agente pregunta por todo, o no pregunta antes de `git push`

Tu versión de OpenCode lee los permisos de otra forma. `python3 ~/.bowser-ai-lite/pruebas/opencode_real.py` comprueba qué entiende tu versión del kit y dice qué falla. Avisa en el repositorio del kit con la salida.

### El agente se confunde o repite cosas

La conversación es demasiado larga. Pídele que actualice el Estado y haga commit, cierra la sesión y abre una nueva con `/bowser-resume`.

## Con git

### "Mensaje de commit inválido"

El mensaje tiene que seguir Conventional Commits: `feat: …`, `fix: …`, `docs: …`, etc. Ver [Controles](08-controles.md#hooks-de-git).

### "No se sube '.env'" o "parece un secreto"

El archivo no debe ir a git. Sácalo de lo que vas a commitear (`git restore --staged <archivo>`) y, si es un `.env`, deja un `.env.example` sin valores reales. Si gitleaks marcó algo que no es un secreto, mira el detalle con `gitleaks protect --staged -v`.

### "es inmutable y ya está en git"

Intentaste cambiar un archivo que figura en `.bowser/inmutables` (por ejemplo, una migración ya aplicada). Crea uno nuevo con el cambio.

### "El Makefile no tiene el objetivo 'check'" o "Push detenido: make check falla"

El hook `pre-push` corre `make check` antes de subir. Arregla lo que falla. Si dice "Define 'test' en el Makefile" o "Define 'lint' en el Makefile", tu `Makefile` viene de la plantilla de la versión 0.13.0 o anterior, que bloqueaba el push hasta definirlos aunque el proyecto no tuviera código: `bowser update` lo cambia por la plantilla nueva si no lo habías tocado, o defínelos tú.

### "'test' y 'lint' siguen sin definir en el Makefile"

`make verify` no deja cerrar una rama que trae código mientras `test` o `lint` sean los de la plantilla, porque `make check` no estaría revisando nada. Defínelos con los comandos reales del proyecto (por ejemplo, en la base mínima, la #1 del roadmap).

### Los hooks no hacen nada

En un clon nuevo hay que activarlos: `make hooks`. Comprueba con `git config core.hooksPath` (debe decir `.githooks`).

## Con make verify

| Mensaje | Qué hacer |
|---|---|
| "Estás en la rama principal" | Cámbiate a la rama de la funcionalidad. `make verify` revisa ramas, no `main` |
| "cambia código sin cambiar pruebas" | Agrega la prueba. Si de verdad no aplica, un commit con `Sin-pruebas: <motivo>` |
| "toca archivos riesgosos … y la rama no tiene plan" | El cambio es grande: plan en `docs/cambios/<nombre>.md` con «Tamaño: grande», aprobado |
| "el plan … se commiteó junto con o después de los archivos riesgosos" | El plan va primero. Rehaz la rama: primero el commit del plan, después el código |
| "el agente revisor no revisó esta rama" | `/bowser-review`. Si lo pediste y sigue saliendo, ver abajo |
| "no se pudo comprobar la revisión en las sesiones de OpenCode" | `opencode` no está en el `PATH` de la terminal donde corres `make verify`, o tu versión exporta las sesiones distinto |
| "⚠ memoria: …" | No bloquea. Actualiza el archivo que nombra, o explica por qué no hace falta |

**El revisor revisó pero `make verify` no lo ve.** Lo busca en las sesiones de OpenCode de esta carpeta desde que se creó la rama, con el nombre de agente `revisor`. Si renombraste el agente, o la revisión se hizo en otra carpeta, no la encuentra. Si nada de eso aplica, tu versión de OpenCode guarda las sesiones en otro formato: avisa en el repositorio del kit.

## Con el comando bowser

### "bowser: command not found"

`~/.local/bin` no está en tu `PATH`. Agrega `export PATH="$HOME/.local/bin:$PATH"` a `~/.bashrc` (o `~/.zshrc`) y abre otra terminal.

### "La copia del kit … tiene cambios locales"

Alguien editó archivos dentro de `~/.bowser-ai-lite`. Míralos con `git -C ~/.bowser-ai-lite status`. Si no los necesitas, `git -C ~/.bowser-ai-lite checkout -- .` y vuelve a correr `bowser update`. El kit no se edita ahí: lo propio de tu proyecto va en tu proyecto.

### "No pude consultar las versiones nuevas"

No hay conexión con GitHub. `bowser update` sigue con la versión que ya tienes.

### Una actualización deshizo un cambio mío

Pasa si se usó `--forzar` en un archivo del kit que habías editado. Tu versión está en `.bowser/respaldo/`:

```bash
diff -u .bowser/respaldo/.github/workflows/bowser.yml .github/workflows/bowser.yml
```

Vuelve a aplicar lo tuyo o, mejor, muévelo a donde el kit lo espera para que no vuelva a pasar (las versiones del CI a `.bowser/versiones`, las reglas a `AGENTS.md`). Revisa también si `docs/memoria/deuda.md` o `decisiones.md` dependían de ese cambio.

### Quiero volver a una versión anterior

`bowser update --version v0.10.0`.

## Con el trabajo a medias

### Se cortó la sesión, se reinició la máquina o cerré OpenCode

No se pierde el trabajo: lo commiteado está en git, lo editado sigue en el disco y la sección Estado del plan dice qué seguía.

| Qué | ¿Sobrevive? |
|---|---|
| Lo commiteado | Sí |
| Archivos editados sin commitear | Sí, pero pueden estar a medias |
| Qué se pidió, qué está hecho y qué sigue (el Estado del plan) | Sí |
| La memoria (`docs/memoria/`) | Sí |
| La conversación | Casi siempre, en las sesiones de OpenCode; la respuesta que se estaba escribiendo, no |

Para seguir: abre OpenCode y busca la sesión anterior en su lista. Si está y no es muy larga, sigue ahí. Si no, sesión nueva y `/bowser-resume`.

Lo único que el kit no protege es el disco: si la máquina se daña, se pierde lo que no se subió. Sube la rama de trabajo al terminar el día.

### Mi pull request choca con la rama principal después de mergear el anterior

La rama nueva salió de la rama de la funcionalidad anterior, no de la principal, y el merge anterior se hizo con squash (un solo commit nuevo en la principal). Git no reconoce que esos commits ya están ahí. Rehaz la rama sobre la principal, dejando fuera los commits de la anterior:

```bash
git fetch origin && git rebase --onto origin/main <rama-anterior> <rama-nueva>
```

Para que no pase: cada funcionalidad empieza desde la rama principal actualizada, después del merge de la anterior. `/bowser-feature` lo hace así y, si estás en otra rama o la anterior no se mergeó, te pregunta de dónde sale.

### No sé en qué iba el proyecto

`/bowser-roadmap`.

Siguiente: [13. Trabajar en el kit](13-trabajar-en-el-kit.md)
