# 13. Trabajar en el kit

[← Inicio](README.md)

Para quien cambia el kit mismo, no un proyecto que lo usa.

## Cómo está organizado

| Carpeta o archivo | Qué hay |
|---|---|
| `plantilla/` | Lo que se copia a cada proyecto: agentes, comandos, hooks, scripts y las semillas de la memoria |
| `catalogo/<tecnología>/SKILL.md` | Las skills de tecnología |
| `instalar.py` | El instalador. `DEL_KIT` lista los archivos del kit y `SEMILLAS` los del proyecto |
| `bin/bowser` | El comando `bowser` (`init`, `update`, `version`) |
| `install.sh` | La instalación en un comando |
| `pruebas/prueba.py` | Las pruebas del kit, con OpenCode simulado |
| `pruebas/opencode_real.py` | Las pruebas contra el OpenCode instalado |
| `.github/workflows/kit.yml` | El CI del kit |
| `docs/` | Esta documentación |
| `PLAN.md` | Por qué el kit es así y qué fases tiene |
| `CHANGELOG.md`, `VERSION` | Los cambios de cada versión y la versión actual |

Todo es Python 3.9+ con solo la biblioteca estándar, bash y Markdown. Nada que instalar para usarlo.

## Pruebas

```bash
python3 pruebas/prueba.py         # todo el kit, con OpenCode simulado: instalación, hooks, verify, costo, distribución
python3 pruebas/opencode_real.py  # contra el OpenCode del PATH: comandos, agentes, permisos y skills (no gasta tokens)
```

`opencode_real.py` instala el kit en un proyecto temporal y le pregunta a OpenCode qué cargó (`opencode debug config` y `opencode debug skill`). Sirve para saber, sin abrir la interfaz, si una versión nueva de OpenCode sigue leyendo el kit.

El CI corre las dos en cada push y pull request, en Linux y macOS con Python 3.9 y 3.13, más `shellcheck` de los scripts, contra la última versión de OpenCode en npm y contra OpenCode 2.0.32 con el instalador oficial, y cada lunes otra vez, para enterarse si una versión nueva deja de leer el kit. Para probar otra: *Actions → Kit → Run workflow* con la versión de `opencode-ai`.

## Agregar o cambiar algo

- **Un comando o agente nuevo**: el archivo en `plantilla/.opencode/…`, su ruta en `DEL_KIT` de `instalar.py`, sus pruebas en `prueba.py` y su página en `docs/`. `opencode_real.py` lo comprueba solo, a partir de `DEL_KIT`.
- **Renombrar un archivo del kit**: basta con cambiarlo en `DEL_KIT`. El instalador retira el viejo de los proyectos (salvo que lo hayan editado).
- **Una semilla nueva**: en `SEMILLAS`. Solo llega a los proyectos que no la tengan.
- **Una regla nueva para el agente**: primero pregúntate si un control la puede comprobar (un hook, `make verify`). Lo que un programa comprueba no se repite en las instrucciones.
- **Algo que aún no se usó en un proyecto real**: no entra. El kit anterior creció con piezas que nadie había necesitado.

## Publicar una versión

Con las pruebas en verde:

1. Sube el número en `VERSION` ([SemVer](https://semver.org/lang/es/): parche para arreglos y documentación, menor para algo nuevo, mayor si un proyecto tiene que cambiar algo al actualizar).
2. Agrega su sección arriba en `CHANGELOG.md`. `bowser update` la muestra a quien actualiza, así que escríbela para esa persona.
3. `git commit -am "chore: versión X.Y.Z"`, `git tag vX.Y.Z` y `git push origin main --tags`.

`bowser update` solo ve versiones etiquetadas (`vX.Y.Z`): lo que está en `main` sin etiqueta no le llega a nadie.

## Usar tu copia sin instalarla

Mientras trabajas en el kit, puedes instalarlo en un proyecto de prueba desde tu copia:

```bash
python3 /ruta/a/tu/copia/bin/bowser init
```
