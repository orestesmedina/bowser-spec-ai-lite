# 6. Agentes

[← Inicio](README.md)

El kit trae tres agentes, en `.opencode/agents/`. Uno trabaja y dos ayudan.

| Agente | Qué hace | Puede editar | Modelo por defecto |
|---|---|---|---|
| `constructor` | Todo el trabajo: entiende, planea, programa, prueba y entrega | Sí | `opencode-go/deepseek-v4.1-flash` |
| `@revisor` | Revisa la rama al final, sin haber visto la conversación | No | `opencode-go/mimo-v2.6-pro` |
| `@explorador` | Lee una zona del código y devuelve un resumen con archivos y líneas | No | `opencode-go/glm-5.3-flash` |

¿Por qué no más agentes? El kit anterior repartía el trabajo en una cadena (analista, arquitecto, programador, probador…) que se pasaba documentos. Cada traspaso perdía contexto y multiplicaba los tokens. Aquí un agente hace el trabajo de punta a punta y los ayudantes solo hacen lo que conviene hacer aparte: leer mucho barato y revisar con ojos frescos.

## constructor

Es el agente que abre OpenCode por defecto (`default_agent` en `opencode.json`). Al empezar lee `.bowser/principios.md` y `AGENTS.md`; antes de escribir código en una tecnología carga su skill; antes de escribir en `docs/`, el estándar de documentación.

**Cómo trabaja:** entiende antes de tocar (si la memoria contradice al código, manda el código), pregunta solo lo ambiguo que cambia el resultado, prueba primero cuando puede, verifica él mismo y no dice que algo funciona sin haberlo visto, hace commits pequeños, y lo que encuentra fuera de la tarea lo anota en `deuda.md` en vez de arreglarlo de paso.

**Permisos:**

| Acción | |
|---|---|
| Editar archivos, correr pruebas, `make`, cualquier comando | Sin preguntar |
| `git push`, `git reset --hard`, `rm -rf`, `docker compose down -v` | **Pregunta** |

**Lo que nunca hace sin que una persona lo pida:** subir cambios, hacer merge o desplegar; saltarse los hooks (`--no-verify`) o desactivar una prueba; cambiar `.bowser/verificacion`, `.githooks/` o el CI para que algo pase; modificar un archivo inmutable ya versionado; guardar secretos en el código o leer `.env`.

## @revisor

Revisa como un ingeniero senior que no escribió el cambio. Recibe el pedido (o el plan) y mira `git diff` contra la rama principal. Revisa en este orden:

1. ¿Hace lo que se pidió, ni más ni menos? ¿Cumple cada criterio de aceptación de los `RF`?
2. Principios y seguridad: inyección, validación en el servidor, escape, autorización, secretos, datos personales.
3. Corrección: errores lógicos, errores ignorados, condiciones de carrera, consultas N+1.
4. Pruebas: ¿prueban el comportamiento real? Puede correrlas.
5. Diseño: ¿respeta las reglas de `modulos.md` (quién puede usar a quién) y los contratos? Romper una frontera sin que el plan lo diga es bloqueante.
6. Convenciones y memoria: ¿el código nuevo sigue las convenciones **decididas** de `convenciones.md`? ¿Deja vieja la memoria?

Responde con un **veredicto** (APROBADO, APROBADO CON CAMBIOS MENORES o CAMBIOS NECESARIOS) y hallazgos en **Bloqueante**, **Importante** y **Sugerencia**, cada uno con archivo, línea y el cambio concreto. No puede editar archivos. `make verify` comprueba, en las sesiones de OpenCode, que el revisor realmente revisó la rama.

## @explorador

Lee una zona del código o responde una pregunta concreta, y devuelve un resumen que permite trabajar sin volver a leerlo todo: qué hace la zona, sus piezas, qué datos usa, quién la llama y qué tiene de raro o riesgoso. Cada afirmación lleva archivo y línea; lo deducido va marcado "(inferido)". Solo lee. El constructor lo usa para leer mucho código sin gastar su propio contexto, y `/bowser-discover` lanza varios en paralelo.

Puedes pedírselo tú también:

```
@explorador ¿dónde se calcula el descuento de los pedidos y qué tablas toca?
```

## Modelos

Cada agente dice su modelo en el campo `model` de su archivo. Para ver cuáles tienes:

```bash
opencode models opencode-go
```

Si usas otro proveedor o un modelo cambió de nombre, edita el campo `model` en `.opencode/agents/*.md`. Al editarlo, el archivo pasa a ser "tuyo": `bowser update` no lo reemplaza y te avisa cuando el kit trae una versión nueva (con `--forzar` lo reemplaza y deja respaldo).

El modelo para tareas chicas de OpenCode (títulos de sesión, resúmenes) está en `small_model` de `opencode.json`.

## Lo propio de tu proyecto

No edites los agentes para meter reglas de tu proyecto: van en `AGENTS.md`, que todos leen. Los agentes son del kit y se reemplazan al actualizar; `AGENTS.md` es tuyo.

Siguiente: [7. Memoria y documentación](07-memoria.md)
