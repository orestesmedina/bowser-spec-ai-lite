---
description: "Ingeniería inversa de un proyecto existente: inventario, módulos, datos, convenciones y deuda, y una prueba de entendimiento. Deja la memoria lista para trabajar con el kit."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

Notas de la persona (puede venir vacío, o nombrar una pasada: inventario, modulos, datos, convenciones, entendimiento): $ARGUMENTS

Tu trabajo es entender un sistema que ya existe y dejarlo escrito, **sin cambiar cómo funciona**. No corriges errores ni mejoras código: lo que encuentres va a la memoria. Lee antes `.bowser/documentacion.md`: dice el formato de todo lo que vas a escribir. Todo lo que afirmes lleva dónde lo viste (`archivo:línea`, tabla o comando); lo que deduces sin haberlo visto se marca "(inferido)".

## 0. Preparar
- Si la carpeta no es un repositorio de git, propón `git init` y un primer commit con el código tal como está, y espera el sí: sin eso no hay forma de volver atrás.
- Trabaja en la rama `docs/descubrimiento`. Lleva el avance en `docs/cambios/descubrimiento.md`: una línea `**Tamaño:** grande` y una sección **Estado** con las cinco pasadas (pendiente, hecha o a medias) y lo que falta preguntar. Si ese archivo ya existe, sigue en la primera pasada pendiente; si la persona nombró una, haz esa.
- Cada pasada termina con un commit (`docs: descubrimiento, <pasada>`) y su Estado al día. Si la sesión se alarga, para al terminar una pasada y propone seguir con `/bowser-resume` en una sesión nueva.
- **Gasta poco:** el detalle de cada módulo lo lee `@explorador` (es más barato); tú lees sus resúmenes y solo abres archivos para confirmar lo importante.

## 1. Inventario
Sin abrir el código a fondo: lenguajes y sus versiones (de `composer.json`, `package.json`, `go.mod`, Dockerfiles…), frameworks, carpetas principales, código de terceros copiado dentro del proyecto (`vendor/`, librerías pegadas), cómo se ejecuta hoy (Docker, un servidor, scripts), si hay pruebas y cómo se corren, y si hay CI.
Escribe:
- **`AGENTS.md`**: "Qué es" (provisional), "Estructura" y "Tecnologías". "Cómo se trabaja" con lo que ya exista; lo que falte se completa en la pasada 5.
- **`docs/memoria/arquitectura.md`**: la tabla de piezas y el diagrama de contexto.
- **`docs/memoria/trampas.md`**: lo que ya se ve que hará perder tiempo (versiones viejas, rutas fijas, dependencias que no están en el repositorio).
- Dile a la persona qué skills del kit corresponden y el comando para instalarlas: `bowser init --skills …`.

## 2. Módulos
Haz la lista de módulos (por carpeta o por responsabilidad). Pide a `@explorador` que resuma cada uno, varios en paralelo, como máximo 8 por ronda. Con sus resúmenes, escribe:
- **`docs/memoria/arquitectura.md`**: el diagrama de contenedores y de 2 a 5 flujos clave, con diagrama de secuencia en los que pasan por varias piezas.
- **`docs/memoria/producto.md`**: las funcionalidades que existen, una fila cada una, en palabras de quien las usa.
- **`docs/producto/requerimientos.md`**: origen "descubierto del código" y la fecha; roles; y un `RF` por comportamiento que existe, con estado `existe`, dónde se vio y sus criterios *Dado / Cuando / Entonces* tal como funciona hoy. Lo que parece un error no se vuelve requisito: va a `deuda.md` o a "Preguntas abiertas".

## 3. Datos
El esquema se **lee, no se recuerda**: de las migraciones, de un script SQL, de los modelos del ORM o, si solo existe en una base viva, de un volcado del esquema que te dé la persona (pídeselo; no leas `.env` ni te conectes a una base de producción). Escribe **`docs/memoria/base-de-datos.md`**: motor y versión, tablas con para qué sirven y sus relaciones, procedimientos, vistas y disparadores, quién usa cada tabla (búscalo en el código) y el diagrama `erDiagram`. Si el esquema tiene más de ~15 tablas, un diagrama por área.

## 4. Convenciones, deuda y controles
- **`docs/memoria/convenciones.md`**: cómo se escribe código en este proyecto, cada regla con un ejemplo real y su archivo.
- **`docs/memoria/deuda.md`**: lo que no cumple `.bowser/principios.md`, sobre todo seguridad (SQL armado con texto, contraseñas sin hash adecuado, secretos en el código, permisos que solo se revisan en el cliente), con su riesgo.
- **`docs/memoria/decisiones.md`**: las decisiones que el código deja ver y alguien podría querer deshacer, marcadas "(inferida)" hasta que la persona las confirme.
- **`.bowser/inmutables`**: las migraciones o scripts ya aplicados.
- **`.bowser/verificacion`**: ajusta `[pruebas]` y `[riesgo]` a cómo se llaman las pruebas y los módulos delicados de este proyecto. Es la única vez que lo cambias por tu cuenta: muestra el cambio a la persona.

## 5. Prueba de entendimiento
1. **Levanta el sistema en local**, con las versiones que usa de verdad (por ejemplo, Docker con la versión real de PHP y de la base de datos). Completa en el `Makefile` los comandos `run`, `test` y `lint` reales y en `AGENTS.md` "Cómo se trabaja". Si para eso agregas archivos de entorno (un `docker-compose.yml`, un Dockerfile), el commit lleva `Sin-pruebas: entorno local del descubrimiento`. No cambies el código del producto para que arranque: si no arranca sin cambiarlo, anótalo en `trampas.md` y pregunta.
2. **Explica un flujo clave paso a paso** a la persona (de la pantalla a la base de datos y de vuelta, con archivos), y pídele que lo confirme o lo corrija. Pregúntale también las decisiones "(inferida)" y las preguntas abiertas más importantes, con tu recomendación.
3. Corrige la memoria con sus respuestas.

## 6. Cerrar
- `make verify` y resuelve lo que marque.
- Pide a `@revisor` que revise la rama contra el código: que elija al menos cinco afirmaciones de la memoria y compruebe que el archivo y la línea citados dicen eso.
- Resume a la persona: qué es el sistema en dos líneas, cuántas funcionalidades, tablas y deudas de riesgo alto encontraste, qué quedó sin resolver y qué propones. Sugiere `/bowser-roadmap` para planear lo que sigue y `/bowser-close` para cerrar esta rama.
- Recuérdale que cambiar un módulo existente empieza por sus **pruebas de caracterización**: `/bowser-feature` las escribe antes de tocar código que no tiene pruebas.
