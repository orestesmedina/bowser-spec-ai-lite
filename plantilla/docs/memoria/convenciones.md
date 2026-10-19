# Convenciones

Cuándo leerlo: antes de escribir código.

<!-- Cómo se escribe código EN ESTE PROYECTO. Lo que se decide está en .bowser/estandares.md.
     Cada regla dice su origen:
     - (decidida, D-NN): la aprobó la persona. El código nuevo la sigue aunque el viejo haga otra cosa.
     - (heredada): se vio en el código y nadie la ha confirmado. Se sigue mientras no haya una decidida.
     Cada regla con un ejemplo real y su archivo. Lo que dicen el formateador o el linter no se repite aquí. Si este
     archivo pasa de ~7 000 caracteres, pártelo por parte del sistema (convenciones-api.md, convenciones-web.md). -->

## Idioma
- <Todo el código en inglés, incluidas variables locales, nombres de prueba y mensajes de error y de log. La
  documentación y los comentarios, en español. (decidida, D-03)>

## Nombres
- <Nombres completos: `affiliate`, no `aff`. Prohibidos `data`, `utils`, `helpers`. (decidida, D-03)>
- <Tablas en plural y snake_case: `pedidos_detalle` (`migrations/0004_pedidos.up.sql`). (heredada)>

## Estructura y patrones
- <Cada dominio tiene handler → service → repository (`internal/pedidos/`). (heredada)>
- <La capa de base de datos se llama `database`. (decidida, D-04)>

## Errores
- <El mensaje dice qué se intentaba y con qué dato: `create order 42: %w`. (decidida, D-03)>

## Bibliotecas que usamos
- <Acceso a datos: sqlc. Validación en el frontend: Zod. (heredada)>

## Pruebas
- <Dónde van, cómo se nombran y cómo se corre una sola.>
