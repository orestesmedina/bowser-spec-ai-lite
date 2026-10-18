---
description: "Muestra en qué va el proyecto (qué es, qué está hecho, qué falta y qué sigue) y, si la persona quiere, replanea el roadmap."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

Notas de la persona (puede venir vacío): $ARGUMENTS

Sirve para retomar un proyecto después de días o semanas sin recordar en qué iba. Primero informas, sin tocar nada; solo replaneas si la persona lo pide.

## 1. Estado del proyecto (solo lectura)
Lee, sin modificar nada:
- `docs/producto/roadmap.md`: funcionalidades, orden y estado.
- `docs/producto/requerimientos.md`: la visión y los `RF` con su estado.
- `docs/memoria/producto.md`: lo que ya existe.
- `docs/memoria/deuda.md`: lo pendiente que no es una funcionalidad.
- `docs/producto/historial.md`: las últimas entregas y su costo.
- Y en git: `git branch --sort=-committerdate` y `git log --oneline -10`, para ver si hay una rama a medias.
- Si hay una funcionalidad en curso (en el roadmap o por la rama), su plan en `docs/cambios/<nombre>.md`, sobre todo la sección **Estado**: qué está hecho, qué sigue y qué falta decidir.

Si algún archivo dice algo distinto de otro (por ejemplo, una funcionalidad "terminada" en el roadmap cuyos `RF` siguen "planeado"), no lo corrijas: anótalo como inconsistencia.

Muéstralo así, en no más de 25 líneas y en palabras de la persona, no de archivos:
- **Qué es:** la visión en una frase.
- **Hecho:** las funcionalidades terminadas, una línea cada una.
- **En curso:** lo que está a medias, con su rama y lo que dice su Estado. Si parece terminada (su Estado lo dice, o no queda nada pendiente) pero no se cerró, dilo y sugiere `/bowser-close`; si no, sugiere `/bowser-resume`.
- **Qué sigue:** las 3 siguientes del roadmap, con su tamaño.
- **Pendientes:** preguntas abiertas de los requerimientos y la deuda de riesgo alto.
- **Inconsistencias**, si las hay.

Si `roadmap.md` y `requerimientos.md` siguen siendo la plantilla, dilo y sugiere `/bowser-idea` (proyecto nuevo) o `/bowser-discover` (proyecto existente). No inventes el estado.

## 2. ¿Replanear?
Pregunta en una línea: "¿Quieres cambiar algo del plan (orden, agregar, partir o descartar funcionalidades)?". Si dice que no, o no responde a eso, **terminas aquí**, sin haber cambiado nada.

## 3. Replanear (solo si dijo que sí)
Con lo que pida, propón los cambios antes de escribir:
- **Agregar:** la funcionalidad, sus `RF` nuevos con criterios de aceptación y su tamaño (grande si toca autenticación, permisos, pagos o datos personales).
- **Partir:** en rebanadas verticales que se puedan probar de punta a punta.
- **Reordenar:** di qué depende de qué antes de mover algo.
- **Descartar:** pasa a `descartada` en el roadmap y los `RF` a `descartado`, con el motivo. No se borran.

Muestra la tabla del roadmap como quedaría y espera su sí. Con eso:
1. Actualiza `docs/producto/roadmap.md` y, si cambiaron requisitos, `docs/producto/requerimientos.md` (siguiendo `.bowser/documentacion.md`).
2. Si la decisión es de las que alguien podría querer deshacer (descartar algo, cambiar la prioridad del negocio), anótala en `docs/memoria/decisiones.md`.
3. Commit: `docs: replanea el roadmap`. Si estás en una rama de funcionalidad a medias, pregunta antes: el replaneo va en la rama principal.
4. Di cuál es la siguiente funcionalidad y cómo empezarla: `/bowser-feature #<n> del roadmap: <nombre>`.
