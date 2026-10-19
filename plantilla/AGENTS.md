# <Nombre del proyecto>

<!-- Plantilla de bowser-ai-lite. Este archivo es del proyecto: edítalo. Mantenlo por debajo de ~100 líneas.
     Aquí van los hechos de ESTE proyecto. El método de trabajo está en .opencode/agents/constructor.md. -->

## Qué es
<Una o dos frases: qué hace el sistema y para quién.>

## Cómo se trabaja con él
| Para… | Comando |
|---|---|
| Levantarlo en local | `make run` |
| Correr todas las pruebas | `make test` |
| Una sola prueba | <por ejemplo: `go test ./internal/usuarios -run TestRegistro`> |
| Revisar formato y estilo | `make lint` |
| Todo lo que corre el CI | `make check` |

<Requisitos de la máquina, puertos, variables de entorno (sin valores secretos: van en `.env`, que no se sube).>

## Estructura
<Las carpetas principales y qué hay en cada una, en 3 a 8 líneas. El detalle está en docs/memoria/arquitectura.md.>

## Reglas que no salen del código
<Solo lo que un agente no puede deducir leyendo el código. Ejemplos:>
- <Las migraciones ya aplicadas no se modifican: se crea una nueva.>
- <Toda consulta a la base de datos pasa por la capa de repositorio.>

## Principios
Los del kit están en `.bowser/principios.md` (seguridad, calidad, datos): valen siempre y se leen al empezar.
Aquí van solo las reglas que este proyecto agrega o endurece. Ninguna puede quitar un principio.

## Tecnologías
<Las del proyecto, con su versión: Go 1.27, React 19, PostgreSQL 16.> Sus estándares están en las skills de
`.opencode/skills/` (se cargan al trabajar con esa tecnología). Si `convenciones.md` dice otra cosa, manda
`convenciones.md`, salvo en seguridad.

## Memoria del proyecto
Lo que el código no dice está en `docs/memoria/`. Lee solo lo que necesites para la tarea:

| Archivo | Léelo cuando… |
|---|---|
| `docs/producto/requerimientos.md` | la tarea agregue o cambie un comportamiento: qué se pidió, para quién y sus criterios |
| `producto.md` | necesites saber qué funcionalidades existen y qué hace cada una |
| `arquitectura.md` | vayas a tocar más de un módulo o no sepas dónde va algo |
| `modulos.md` | vayas a tocar un módulo que no conoces o agregar uno: para qué sirve cada uno y quién puede usar a quién |
| `base-de-datos.md` | la tarea toque tablas, consultas o migraciones |
| `decisiones.md` | vayas a cambiar algo que parece raro: puede tener un motivo |
| `trampas.md` | antes de levantar, probar o desplegar |
| `convenciones.md` | vayas a escribir código |
| `deuda.md` | toques un módulo con deuda conocida |

Si la memoria contradice al código, manda el código: corrígela en el mismo cambio. Para escribir o cambiar
cualquier documento de `docs/`, sigue `.bowser/documentacion.md` (formato de requisitos, diagramas y decisiones).
