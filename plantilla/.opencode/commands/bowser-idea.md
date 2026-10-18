---
description: "Convierte una idea en un proyecto listo para construir: requerimientos, arquitectura inicial, decisiones y roadmap. No escribe código."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

La idea de la persona: $ARGUMENTS

Tu trabajo aquí es de producto y arquitectura, no de programación: **no escribes código ni configuras herramientas**. Lo que sale de este comando son documentos que la persona aprueba, y de ahí en adelante cada funcionalidad se construye con `/bowser-feature`. Lee antes `.bowser/documentacion.md`: dice el formato de todo lo que vas a escribir.

## 0. Comprobar el punto de partida
Mira la carpeta. Si ya hay código del producto (más allá de lo que instaló el kit), detente: este comando es para empezar desde cero. Dile a la persona que para un proyecto existente está `/bowser-discover`, que escribe los documentos leyendo el código, y pregunta si quiere seguir de todos modos.
Si `docs/producto/requerimientos.md` ya tiene contenido real (no la plantilla), muéstralo y pregunta si lo reemplazas o lo completas.

## 1. Entrevista
Pregunta en rondas cortas: **como máximo 5 preguntas por ronda y 3 rondas**. Cada pregunta lleva tu recomendación, para que la persona pueda responder "sí" o "la 2 no, la 4 sí". No preguntes lo que puedas decidir tú con un supuesto razonable: decídelo y dilo.

Lo que necesitas saber al terminar:
- **Problema y para quién:** qué duele hoy, quiénes lo usarán y con qué roles.
- **Cómo sabremos que funciona:** 1 a 3 resultados medibles.
- **La primera versión:** lo mínimo que ya sirve a alguien. Empuja a que sea chica; lo demás va al roadmap como "después".
- **Qué no incluye**, dicho explícitamente.
- **Datos e integraciones:** qué se guarda (sobre todo datos personales o pagos) y con qué sistemas externos habla.
- **Restricciones:** dónde va a correr, cuántos usuarios, presupuesto, tecnología obligada, leyes.
- **Tecnología:** recomienda una pila sencilla, preferiblemente con skills del kit (`go`, `react`, `postgres`, `php`, `mysql`, `web`), y explica en una línea por qué. Si la persona ya tiene una preferencia, úsala salvo que choque con una restricción.

Lo que quede sin respuesta va a "Preguntas abiertas", con tu recomendación. No lo inventes.

## 2. Escribir
Con las respuestas, escribe en este orden y siguiendo `.bowser/documentacion.md`:
1. **`docs/producto/requerimientos.md`**: origen "idea" y la fecha de hoy; visión, roles, alcance, requisitos `RF-NN` con criterios *Dado / Cuando / Entonces* (estado `planeado`), `RNF-NN` comprobables, restricciones, preguntas abiertas y glosario.
2. **`docs/memoria/arquitectura.md`**: diagrama de contexto y de contenedores con la pila elegida, y la tabla de piezas con las carpetas que tendrá el proyecto. Los flujos clave se dibujan cuando se construyan.
3. **`docs/memoria/decisiones.md`**: una entrada por decisión tomada en la entrevista que alguien podría querer deshacer (la pila, el hosting, lo que se dejó fuera a propósito).
4. **`docs/producto/roadmap.md`**: funcionalidades en orden, cada una con sus `RF`, su tamaño estimado y estado `pendiente`.
   - La **#1 es siempre la base mínima**: el proyecto se levanta con `make run`, tiene una prueba que pasa, `run`/`test`/`lint`/`check` definidos en el `Makefile`, `ci-setup` si el CI lo necesita, y `AGENTS.md` dice cómo correrlo. Sin funcionalidades de negocio.
   - Después, rebanadas verticales: cada una se puede probar de punta a punta (pantalla, lógica y datos) y entrega algo que una persona nota. Nada de "hacer toda la base de datos" como funcionalidad.
   - Lo que toque autenticación, permisos, pagos o datos personales se marca **grande** desde ya.
   - Lo que quedó para "después" va al final, con estado `pausada`.
5. **`AGENTS.md`**: completa "Qué es" y "Tecnologías". "Cómo se trabaja" y "Estructura" los completa la funcionalidad #1.

## 3. Aprobar
Muestra a la persona, en no más de 20 líneas: la visión en una frase, los roles, los `RF` de la primera versión (solo id y título), lo que queda fuera, la pila y el roadmap. Pregunta si lo aprueba así o qué cambia. Ajusta hasta que diga que sí. No sigas sin esa aprobación.

## 4. Cerrar
1. Si el repositorio aún no tiene commits, primero uno con lo que instaló el kit: `chore: instala bowser-ai-lite`. Después, el de los documentos: `docs: requerimientos, arquitectura y roadmap iniciales`.
2. Dile a la persona los dos pasos siguientes, con los comandos exactos:
   - Instalar las skills de la pila elegida: `bowser init --skills <las de la pila>`.
   - Empezar la base mínima en una sesión nueva: `/bowser-feature #1 del roadmap: base mínima`.
