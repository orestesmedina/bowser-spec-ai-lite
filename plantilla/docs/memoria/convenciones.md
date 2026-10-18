# Convenciones

Cuándo leerlo: antes de escribir código.

<!-- Cómo se escribe código EN ESTE PROYECTO, sacado de leer el código. Cada regla con un ejemplo real
     y su archivo. Lo que dicen el formateador o el linter no se repite aquí. Si este archivo pasa de
     ~7 000 caracteres, pártelo por parte del sistema (convenciones-api.md, convenciones-web.md). -->

## Nombres
- <Tablas en plural y snake_case: `pedidos_detalle` (`migrations/0004_pedidos.up.sql`).>

## Estructura y patrones
- <Cada dominio tiene handler → service → repository (`internal/pedidos/`).>

## Bibliotecas que usamos
- <Acceso a datos: sqlc. Validación en el frontend: Zod.>

## Pruebas
- <Dónde van, cómo se nombran y cómo se corre una sola.>
