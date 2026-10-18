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
3. Pregunta si actualiza. Solo con un sí, ejecuta `bowser update` (si pidió reemplazar también lo editado: `bowser update --forzar`).
4. Si hubo cambios, haz commit: `chore: actualiza bowser-ai-lite a <versión>`. Si estás en una rama de funcionalidad a medias, pregunta antes: la actualización va en la rama principal.
5. Recuérdale que **cierre OpenCode y lo vuelva a abrir**: los comandos y agentes nuevos solo se cargan al arrancar.
