---
description: "Retoma una funcionalidad a medias después de un corte, un reinicio o en una sesión nueva."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

Notas de la persona (puede venir vacío): $ARGUMENTS

Una sesión anterior quedó a medias. No confíes en lo que creas recordar: reconstruye el estado desde el disco.

1. **Dónde estás.** `git branch --show-current`, `git log --oneline <rama-principal>..HEAD` y `git status`. Si estás en la rama principal, busca la rama de trabajo más reciente (`git branch --sort=-committerdate`) y pregunta antes de cambiarte.
2. **Qué se pidió y qué faltaba.** Lee `docs/cambios/<nombre>.md` (el nombre de la rama sin `feat/` o `fix/`), sobre todo su sección **Estado**. En un cambio pequeño sin plan, los mensajes de commit son el estado.
3. **Lo que no se commiteó.** Revisa `git diff` y los archivos sin seguimiento: es trabajo de la sesión cortada que sobrevivió en el disco, pero puede estar a medias. Corre las pruebas para saber si está sano. No lo descartes sin preguntar.
4. **Muéstralo a la persona en pocas líneas:** qué está hecho (commits), qué quedó sin commitear y si pasa las pruebas, qué sigue según el Estado y qué decisión estaba pendiente. Pregunta si sigues desde ahí.
5. Con su respuesta, actualiza el Estado si hace falta y continúa con el paso que corresponda de `/bowser-feature`.
