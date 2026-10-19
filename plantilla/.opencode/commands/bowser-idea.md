---
description: "Convierte una idea en un proyecto listo para construir: requerimientos, estándares, diseño inicial (datos, módulos y contratos), decisiones y roadmap, aprobados por la persona. No escribe código."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

La idea de la persona: $ARGUMENTS

Tu trabajo aquí es de producto y arquitectura, no de programación: **no escribes código ni configuras herramientas**. Lo que sale de este comando son documentos que la persona aprueba, y de ahí en adelante cada funcionalidad se construye con `/bowser-feature`. Lee antes `.bowser/documentacion.md`: dice el formato de todo lo que vas a escribir.

Un requerimiento dice **qué** hace el sistema; el diseño dice **cómo** está hecho. Si nadie decide el cómo antes de programar, lo decide el agente funcionalidad por funcionalidad, por el camino más corto, y la persona deja de saber cómo está construido su sistema. Por eso este comando termina con un diseño que la persona revisó y aprobó: tablas, módulos, fronteras y contratos.

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
- **Datos e integraciones:** qué se guarda (sobre todo datos personales o pagos), cuánto va a crecer y con qué sistemas externos habla.
- **Restricciones:** dónde va a correr, cuántos usuarios, presupuesto, tecnología obligada, leyes.
- **Tecnología:** recomienda una pila sencilla, preferiblemente con skills del kit (`go`, `react`, `postgres`, `php`, `mysql`, `web`), y explica en una línea por qué. Si la persona ya tiene una preferencia, úsala salvo que choque con una restricción.

Lo que quede sin respuesta va a "Preguntas abiertas", con tu recomendación. No lo inventes.

## 2. Estándares
Sigue `.bowser/estandares.md`, en una sola ronda, con la recomendación de la skill de cada tecnología de la pila (o de la guía oficial del lenguaje, si no hay skill). No hay código todavía, así que no hay "lo que hay hoy": pregunta sobre todo el idioma del código y de los textos, los nombres, cómo se llama cada capa (con los nombres que la persona usa en sus otros proyectos) y la estructura de carpetas, mostrando el árbol de 2 o 3 opciones si la pila no tiene framework. Muestra el resultado en no más de 15 líneas y espera su sí.

## 3. Diseño
Solo de lo que necesita la primera versión: lo que quedó para "después" no se diseña todavía. Muéstralo **por partes** y espera el sí de cada una, porque es lo que la persona va a tener que entender cuando el código exista. Como máximo una ronda de ajustes por parte; lo que no se pueda decidir todavía va a "Preguntas abiertas" con tu recomendación, en vez de un diseño inventado.
1. **Modelo de datos**: el `erDiagram` de las entidades principales y la tabla de tablas con sus columnas clave, llaves, los índices que importan y cuáles van a crecer mucho (y qué se hace con eso: separar el histórico, particionar, archivar).
2. **Módulos y fronteras**: los módulos con su propósito, el diagrama de quién usa a quién y las reglas de quién **no** puede usar a quién ("Pagos no lee las tablas de Usuarios: pasa por su servicio"). Los nombres de capa son los de la fase 2.
3. **Contratos**: las rutas o interfaces principales entre módulos y con el exterior, con lo que reciben y lo que devuelven. Solo las de la primera versión.

## 4. Escribir
Con lo aprobado, escribe en este orden y siguiendo `.bowser/documentacion.md`:
1. **`docs/producto/requerimientos.md`**: origen "idea" y la fecha de hoy; visión, roles, alcance, requisitos `RF-NN` con criterios *Dado / Cuando / Entonces* (estado `planeado`), `RNF-NN` comprobables, restricciones, preguntas abiertas y glosario.
2. **`docs/memoria/convenciones.md`**: las reglas de la fase 2, cada una **(decidida, D-NN)**.
3. **`docs/memoria/base-de-datos.md`**: el modelo de datos de la fase 3, con cada tabla en estado `diseñada`. La funcionalidad que cree su migración la pasa a `existe`.
4. **`docs/memoria/modulos.md`**: los módulos, sus reglas (marcadas como nuevas, con su `D-NN`) y el contrato de cada uno.
5. **`docs/memoria/arquitectura.md`**: diagrama de contexto y de contenedores con la pila elegida, y la tabla de piezas con las carpetas que tendrá el proyecto. Enlaza a `modulos.md`; los flujos clave se dibujan cuando se construyan.
6. **`docs/memoria/decisiones.md`**: una entrada por decisión tomada en la entrevista, los estándares o el diseño que alguien podría querer deshacer (la pila, el hosting, lo que se dejó fuera a propósito, una frontera entre módulos).
7. **`docs/producto/roadmap.md`**: funcionalidades en orden, cada una con sus `RF`, las tablas, módulos y contratos del diseño que construye, su tamaño estimado y estado `pendiente`.
   - La **#1 es siempre la base mínima**: el proyecto se levanta con `make run`, tiene una prueba que pasa, `run`/`test`/`lint`/`check` definidos en el `Makefile`, `ci-setup` si el CI lo necesita, el árbol de carpetas acordado en la fase 2 y `AGENTS.md` dice cómo correrlo. Sin funcionalidades de negocio.
   - Después, rebanadas verticales: cada una se puede probar de punta a punta (pantalla, lógica y datos) y entrega algo que una persona nota. Nada de "hacer toda la base de datos" como funcionalidad: cada una crea las tablas diseñadas que usa.
   - Lo que toque autenticación, permisos, pagos o datos personales se marca **grande** desde ya.
   - Lo que quedó para "después" va al final, con estado `pausada`.
8. **`AGENTS.md`**: completa "Qué es", "Tecnologías" y "Estructura" (el árbol acordado). "Cómo se trabaja" lo completa la funcionalidad #1.

## 5. Aprobar
Muestra a la persona, en no más de 20 líneas: la visión en una frase, los roles, los `RF` de la primera versión (solo id y título), lo que queda fuera, la pila, cuántas tablas y módulos tiene el diseño y el roadmap. Pregunta si lo aprueba así o qué cambia. Ajusta hasta que diga que sí. No sigas sin esa aprobación.

## 6. Cerrar
1. Si el repositorio aún no tiene commits, primero uno con lo que instaló el kit: `chore: instala bowser-ai-lite`. Después, el de los documentos: `docs: requerimientos, diseño y roadmap iniciales`.
2. Dile a la persona los dos pasos siguientes, con los comandos exactos:
   - Instalar las skills de la pila elegida: `bowser init --skills <las de la pila>`.
   - Empezar la base mínima en una sesión nueva: `/bowser-feature #1 del roadmap: base mínima`.
