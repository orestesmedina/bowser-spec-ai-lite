---
description: "Construir una funcionalidad, corregir un error o hacer un cambio, con la ceremonia que corresponde a su tamaño."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

Lo que la persona quiere: $ARGUMENTS

## 1. Tamaño
Lee lo necesario de `AGENTS.md`, `docs/memoria/` y el código para proponer un tamaño, y pide que lo confirme en una línea:

- **Pequeño** (un error, un texto, un ajuste que no cambia datos ni permisos): vas directo al paso 3.
- **Normal**: escribes un plan corto y sigues.
- **Grande o riesgoso** (datos de clientes, pagos, permisos, seguridad, cambios de esquema grandes, reconstruir un módulo): escribes spec y plan, y **esperas su aprobación** antes de programar.

Si el cambio va a tocar un archivo de la sección `[riesgo]` de `.bowser/verificacion` (migraciones, autenticación, permisos, pagos…), es grande aunque parezca pequeño: `make verify` lo exige.

Si el pedido es ambiguo en algo que cambia el resultado, pregúntalo junto con el tamaño.

## 2. Plan (normal y grande)
Crea la rama `feat/<nombre-corto>` (o `fix/…`) desde la rama principal actualizada (por ejemplo, `git switch main && git pull --ff-only`), sin preguntar cuando estás en la rama principal y no hay otra funcionalidad a medias. Si estás en otra rama o hay una funcionalidad sin mergear, **pregunta de dónde sale la rama nueva**, recomendando la principal: si sale de otra rama y esa se mergea con squash, la nueva va a chocar con la principal y habrá que rehacerla sobre ella (`git rebase --onto main <rama-anterior>`). Anota la base elegida en el plan. Escribe `docs/cambios/<nombre-corto>.md` (el mismo nombre de la rama), de una página como máximo. Empieza con la línea `**Tamaño:** normal` o `**Tamaño:** grande`, y haz su commit (`docs: plan de <nombre-corto>`) **antes** de tocar código:

- **Qué se pide**, en palabras de la persona, y qué queda fuera. Qué requisitos de `docs/producto/requerimientos.md` cubre (`RF-NN`) o cuáles agrega, con sus criterios de aceptación.
- **Cómo se hace:** archivos o módulos que cambian, datos que cambian (tablas, columnas, migraciones) y por qué así.
- **Cómo se comprueba:** qué pruebas y qué se verá funcionando.
- (Grande) **Diagramas** de lo nuevo (piezas, tablas, flujo o estados), en Mermaid según `.bowser/documentacion.md`.
- (Grande) **Riesgos** y cómo se revierte.
- **Estado**, al final: qué está hecho, qué sigue y qué falta decidir. Lo actualizas y commiteas con cada paso terminado: si la sesión se corta, `/bowser-resume` sigue desde aquí.

En un cambio normal muestras el plan en 5 a 10 líneas y sigues, salvo que la persona te frene. En uno grande te detienes hasta que diga que sí.

## 3. Construir
Sigue "Cómo trabajas" de tus instrucciones: prueba primero cuando puedas, corre la prueba puntual mientras trabajas, commits pequeños. En un cambio pequeño la rama es `fix/<nombre-corto>`, también desde la rama principal actualizada, y el plan no hace falta.

**Código existente sin pruebas:** antes de cambiarlo, escribe sus **pruebas de caracterización**: fijan cómo se comporta hoy, aunque parezca raro o equivocado, con los casos que el cambio puede afectar. Van en su propio commit (`test: caracteriza <módulo>`), antes del cambio, y tienen que pasar sin tocar el código. Si una muestra un comportamiento que parece un error, no lo corrijas de paso: anótalo en `deuda.md` y pregunta. Al reconstruir un módulo entero, estas pruebas son las que dicen que el resto del sistema no notó la diferencia: se reemplaza por partes, cada parte con las pruebas en verde.

## 4. Comprobar
- `make check` en verde.
- Si hay interfaz o API: levántalo (`make run`) y comprueba el flujo de punta a punta. Di exactamente qué viste.

## 5. Revisar
Pide a `@revisor` que revise la rama contra el pedido (y el plan, si lo hay). Es obligatorio en todos los tamaños: `/bowser-close` comprueba en las sesiones de OpenCode que el revisor revisó la rama. Corrige los bloqueantes y los importantes que tengan sentido. Si después de dos vueltas sigue habiendo bloqueantes, detente y explica a la persona qué falta y qué decisión necesitas.

## 6. Entregar
Corre `make verify` y resuelve lo que marque (sin tocar `.bowser/verificacion`). Resume: qué cambió en lenguaje simple, cómo lo comprobaste (incluida la salida de `make verify`), qué dijo el revisor y qué corregiste, y qué propones cambiar en `docs/memoria/`. Termina diciendo: "Si está bien, escribe /bowser-close".
