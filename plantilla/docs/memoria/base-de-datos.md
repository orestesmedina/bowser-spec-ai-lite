# Base de datos

Cuándo leerlo: cuando la tarea toque tablas, consultas, procedimientos o migraciones.

<!-- En un proyecto existente se genera leyendo el esquema real (migraciones, script SQL o la base), no de memoria.
     En uno nuevo, /bowser-idea escribe aquí el diseño aprobado, con cada tabla en estado "diseñada"; la funcionalidad
     que crea su migración la pasa a "existe", leyendo el esquema real. Si una tabla cambia, este archivo cambia en el
     mismo commit. -->

Motor: <PostgreSQL 16>. Dónde está el esquema: <`backend/migrations/`>.

## Tablas

| Tabla | Para qué | Columnas clave | Relaciones | Estado |
|---|---|---|---|---|
| <usuarios> | <Cuentas de acceso> | <id, correo (único), creado_en> | <— > | <existe \| diseñada> |

## Procedimientos, vistas y disparadores
<!-- Si los hay: nombre, qué hace y quién lo llama. -->

## Diagrama

```mermaid
erDiagram
  USUARIOS ||--o{ SESIONES : tiene
```
