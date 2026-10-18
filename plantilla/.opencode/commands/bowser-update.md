---
description: "Actualiza el kit bowser-ai-lite en este proyecto a la última versión publicada."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

Notas de la persona (puede venir vacío): $ARGUMENTS

1. Ejecuta `bowser update --verificar`. Si el comando `bowser` no existe, dile a la persona que instale el kit con
   `curl -fsSL https://raw.githubusercontent.com/orestesmedina/bowser-spec-ai-lite/main/install.sh | bash` y termina.
2. Muéstrale en pocas líneas: de qué versión a cuál pasa, lo más importante de los cambios (del CHANGELOG que imprimió) y
   qué archivos del proyecto cambiarían. Si hay avisos de archivos editados que no se van a reemplazar, menciónalos.
   Si ya está en la última versión, dilo y termina.
   Si un archivo editado por el proyecto trae cambios del kit, corre el `diff -u` que muestra el aviso y explica en
   una línea qué trae el kit y qué tiene el proyecto que el kit no tiene.
3. Pregunta si actualiza. Solo con un sí, ejecuta `bowser update`. **No uses `--forzar` por tu cuenta**: borra lo que el
   proyecto cambió en ese archivo. Si un archivo editado trae cambios del kit que hacen falta, propón pasarlos a mano.
   Si la persona elige `--forzar`, compara cada respaldo de `.bowser/respaldo/` con el archivo nuevo y vuelve a aplicar
   lo que era del proyecto (o muévelo a donde el kit lo espera ahora, por ejemplo las versiones del CI a
   `.bowser/versiones`). Después revisa si `docs/memoria/` (sobre todo `deuda.md` y `decisiones.md`) dependía de lo que
   cambió.
4. Si hubo cambios, haz commit: `chore: actualiza bowser-ai-lite a <versión>`. Si estás en una rama de funcionalidad a medias, pregunta antes: la actualización va en la rama principal.
5. Recuérdale que **cierre OpenCode y lo vuelva a abrir**: los comandos y agentes nuevos solo se cargan al arrancar. Con OpenCode 2 (`opencode --version`), antes de abrirlo: `opencode reload`, porque su servicio de fondo sigue con la configuración de antes.
