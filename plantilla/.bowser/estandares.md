# Estándares del proyecto: qué se le pregunta a la persona

<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. Dice QUÉ se decide; lo decidido vive en
     docs/memoria/convenciones.md, que es del proyecto. Lo usa /bowser-discover (y /bowser-idea en un proyecto nuevo). -->

Son las mismas preguntas para cualquier lenguaje (PHP, Go, TypeScript, Rust, C#, SQL…). Lo que impone el lenguaje
o su formateador (mayúsculas, `camelCase` o `snake_case`, sangría) no se pregunta: lo dice la skill de esa
tecnología o la herramienta.

## Cómo se pregunta
- Una sola ronda, con todas las preguntas que el código o la persona no hayan respondido ya.
- Cada pregunta trae **lo que hay hoy** (con un ejemplo y su archivo) y **tu recomendación**, para que la persona
  pueda responder "sí a todo" o "la 3 no, prefiero la b".
- Si la persona responde solo algunas, para las demás vale tu recomendación: dilo y anótala como **decidida** solo si
  la persona no la objeta al ver el resumen.
- La recomendación sale de la skill de la tecnología. Si no hay skill, de la guía oficial del lenguaje, y lo dices.

## Las preguntas

| # | Tema | Qué se decide | Recomendación habitual |
|---|---|---|---|
| 1 | Idioma del código | De tipos, funciones, variables locales, constantes y nombres de prueba | Inglés en todo el código |
| 2 | Idioma de los textos | Comentarios y documentación; mensajes de error y de log; lo que ve una persona | Documentación en el idioma del equipo; errores y logs en el del código; lo que ve una persona, desde archivos de idioma |
| 3 | Nombres | Qué tan descriptivos, qué abreviaturas se permiten, cuáles se prohíben | Nombres completos; abreviatura solo si es del dominio o del lenguaje (`id`, `url`, `ctx`); prohibidos `data`, `info`, `tmp`, `utils`, `helpers`, `misc` |
| 4 | Nombre de cada capa | Cómo se llaman la capa de base de datos, la de lógica de negocio y la de entrada (HTTP, consola, colas) | Los nombres que la persona ya usa en sus otros proyectos (`database`, `services`, `http`…), si el lenguaje no lo desaconseja |
| 5 | Estructura de carpetas | Por capas, por dominio o por funcionalidad | Con framework, la del framework; sin framework, muestra 2 o 3 opciones con su árbol y lo que costaría cambiar |
| 6 | Dónde va cada cosa | Lógica de negocio, acceso a datos, validación, permisos, trabajo en segundo plano | Entrada fina → lógica → datos; la validación y los permisos en el servidor |
| 7 | Errores | Qué recibe quien llama (forma y códigos), qué va al log, qué contexto lleva cada mensaje | El mensaje dice qué se intentaba y con qué dato; el detalle interno solo en el log |
| 8 | Base de datos | Nombres de tablas y columnas (singular o plural, idioma), llaves, índices, borrado lógico o físico | Lo que diga la skill del motor |
| 9 | Pruebas | Dónde van, cómo se nombran, qué es obligatorio probar | Lo que diga la skill; el nombre dice qué comportamiento prueba |
| 10 | El código que ya existe | Qué se hace con lo que no cumple una regla nueva | Se ajusta solo cuando una funcionalidad toca ese archivo, en un commit `refactor:` aparte y con las pruebas en verde; nunca mezclado con un cambio de comportamiento |

## Qué se escribe después
- **`docs/memoria/convenciones.md`**: cada regla con su origen, **decidida** (la aprobó la persona, con la fecha y la
  `D-NN`) o **heredada** (se vio en el código y nadie la confirmó). El código nuevo sigue las decididas; si sobre un
  tema solo hay una heredada, se sigue esa.
- **`docs/memoria/decisiones.md`**: una `D-NN` por cada cambio de rumbo (una regla decidida distinta de lo que el
  código hace hoy).
- **`docs/memoria/deuda.md`**: el código que no cumple una regla decidida, con sus archivos, para ajustarlo al tocarlo.
