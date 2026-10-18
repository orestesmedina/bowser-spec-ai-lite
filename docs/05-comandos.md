# 5. Comandos

[← Inicio](README.md)

Comandos de OpenCode: [/bowser-idea](#bowser-idea) · [/bowser-discover](#bowser-discover) · [/bowser-roadmap](#bowser-roadmap) · [/bowser-feature](#bowser-feature) · [/bowser-review](#bowser-review) · [/bowser-close](#bowser-close) · [/bowser-resume](#bowser-resume) · [/bowser-cost](#bowser-cost) · [/bowser-update](#bowser-update)

En la terminal: [bowser](#el-comando-bowser) · [make](#comandos-de-make)

Todos corren con el agente `constructor`. Lo que escribas después del nombre del comando le llega como tus notas.

---

## /bowser-idea

**Para:** convertir una idea en un proyecto listo para construir. **No escribe código.**

**Cuándo:** la carpeta está vacía (o solo tiene lo que instaló el kit). Si ya hay código, se detiene y te sugiere `/bowser-discover`.

```
/bowser-idea un sistema para que una clínica lleve el historial de vacunas de sus pacientes
```

**Qué hace:**
1. **Entrevista**: como máximo 3 rondas de 5 preguntas. Cada una trae su recomendación. Lo que puede decidir con un supuesto razonable, lo decide y te lo dice. Necesita saber: el problema y para quién, cómo sabrán que funciona, lo mínimo que ya sirve, qué no incluye, qué datos guarda (sobre todo personales o pagos), las restricciones y la tecnología.
2. **Escribe**, siguiendo el [estándar de documentación](07-memoria.md#el-formato): requerimientos, arquitectura (contexto y contenedores), decisiones y roadmap. La funcionalidad #1 del roadmap es siempre la **base mínima**: el proyecto corre, tiene una prueba y su `Makefile` está completo, sin funcionalidades de negocio. Después vienen rebanadas que se pueden probar de punta a punta. Lo que toca autenticación, permisos, pagos o datos personales queda marcado como grande.
3. **Te pide aprobación** con un resumen de no más de 20 líneas. No sigue sin tu sí.
4. **Commitea** y te dice qué skills instalar y cómo empezar la #1.

**Deja escrito:** `docs/producto/requerimientos.md`, `docs/producto/roadmap.md`, `docs/memoria/arquitectura.md`, `docs/memoria/decisiones.md` y parte de `AGENTS.md`.

---

## /bowser-discover

**Para:** entender un sistema que ya existe y dejarlo documentado, **sin cambiar cómo funciona**. Es ingeniería inversa.

**Cuándo:** heredaste un proyecto, o el tuyo nunca tuvo memoria. Hazlo antes de la primera funcionalidad.

```
/bowser-discover
/bowser-discover datos          # solo esa pasada
```

**Qué hace:** trabaja en la rama `docs/descubrimiento` y lleva su avance en `docs/cambios/descubrimiento.md`. Cada pasada termina con un commit; si la sesión se corta o se alarga, la siguiente vez sigue en la primera pendiente. Todo lo que afirma lleva dónde lo vio (`archivo:línea`); lo que deduce sin verlo va marcado "(inferido)". El detalle de los módulos lo lee `@explorador`, que es más barato.

| Pasada | Qué averigua | Dónde lo escribe |
|---|---|---|
| 0. Preparar | Si no hay git, te propone `git init` y un primer commit antes de nada | |
| 1. Inventario | Lenguajes y versiones, frameworks, carpetas, código de terceros copiado, cómo se corre hoy, si hay pruebas y CI. Te dice qué skills instalar | `AGENTS.md`, `arquitectura.md` (piezas y contexto), `trampas.md` |
| 2. Módulos | Qué hace cada módulo (hasta 8 a la vez con `@explorador`), los flujos clave | `arquitectura.md` (contenedores y flujos), `producto.md`, `requerimientos.md` (un `RF` con estado `existe` por comportamiento) |
| 3. Datos | El esquema, leído de migraciones, SQL, modelos o de un volcado que le pases. **Nunca lee `.env` ni se conecta a producción** | `base-de-datos.md` con su `erDiagram` |
| 4. Convenciones y deuda | Cómo se escribe código aquí, qué no cumple los principios (sobre todo seguridad), qué decisiones deja ver el código | `convenciones.md`, `deuda.md`, `decisiones.md` (marcadas "(inferida)"), `.bowser/inmutables`, `.bowser/verificacion` (te muestra el cambio) |
| 5. Entendimiento | Levanta el sistema en local con sus versiones reales y completa el `Makefile`. Te explica un flujo paso a paso y te pregunta las decisiones inferidas | Corrige la memoria con tus respuestas |
| 6. Cerrar | `make verify`; `@revisor` comprueba al menos cinco afirmaciones contra el código | Resumen: qué es, cuántas funcionalidades, tablas y deudas graves |

Lo que parece un error no se vuelve requisito: va a `deuda.md` o a "Preguntas abiertas". Si el sistema no arranca sin cambiar su código, no lo cambia: lo anota y te pregunta.

---

## /bowser-roadmap

**Para:** saber en qué va el proyecto y, si quieres, cambiar el plan.

**Cuándo:** vuelves después de días o semanas, o quieres agregar, partir, reordenar o descartar funcionalidades.

```
/bowser-roadmap
/bowser-roadmap quiero meter pagos con tarjeta antes de los reportes
```

**Qué hace:**
1. **Informa sin tocar nada** (no más de 25 líneas): qué es, qué está hecho, qué está a medias (con lo que dice el Estado de su plan; si parece terminada te sugiere `/bowser-close`, si no `/bowser-resume`), las tres que siguen, las preguntas abiertas, la deuda de riesgo alto y las contradicciones entre documentos.
2. **Pregunta si quieres replanear.** Si dices que no, termina sin haber cambiado nada.
3. **Si dices que sí**, propone los cambios, te muestra la tabla del roadmap como quedaría y espera tu sí. Descartar no borra: marca la funcionalidad como `descartada` y sus `RF` como `descartado`, con el motivo. Commitea en la rama principal.

---

## /bowser-feature

**Para:** construir una funcionalidad, corregir un error o hacer cualquier cambio. Es el comando que más vas a usar.

```
/bowser-feature #2 del roadmap: agenda del taller
/bowser-feature el reporte de ventas tarda 30 segundos con más de mil pedidos
/bowser-feature cambia el color del botón principal a verde
```

**Qué hace:**

1. **Tamaño.** Lee lo necesario y te propone pequeño, normal o grande; lo confirmas en una línea. Si algo ambiguo cambia el resultado, lo pregunta aquí. Si el cambio toca un archivo riesgoso (migraciones, autenticación, permisos, pagos), es grande sí o sí.
2. **Plan** (normal y grande). Rama `feat/<nombre>` o `fix/<nombre>` y el plan en `docs/cambios/<nombre>.md`, de una página, commiteado **antes** del código: qué se pide y qué queda fuera, qué `RF` cubre, cómo se hace, cómo se comprueba, y en uno grande, diagramas y riesgos. Al final, la sección **Estado**, que se mantiene al día con cada paso. En uno normal te lo muestra y sigue; en uno grande **espera tu sí**.
3. **Construir.** Prueba primero cuando puede, commits pequeños con Conventional Commits. Si va a cambiar código existente que no tiene pruebas, primero escribe **pruebas de caracterización** (cómo funciona hoy, aunque parezca raro) en su propio commit.
4. **Comprobar.** `make check` en verde. Si hay interfaz o API, levanta la app y comprueba el flujo de punta a punta, y te dice qué vio.
5. **Revisar.** `@revisor` revisa la rama, en todos los tamaños. Corrige lo bloqueante. Si tras dos vueltas sigue habiendo bloqueantes, se detiene y te explica qué decisión necesita.
6. **Entregar.** `make verify` y un resumen: qué cambió, cómo lo comprobó, qué dijo el revisor y qué propone cambiar en la memoria. Termina con "Si está bien, escribe /bowser-close".

---

## /bowser-review

**Para:** una revisión independiente de la rama, cuando quieres verla tú antes de que el agente corrija.

```
/bowser-review
/bowser-review fíjate sobre todo en los permisos
```

Le pasa a `@revisor` el pedido y el plan. **No corrige nada**: te muestra el veredicto (APROBADO, APROBADO CON CAMBIOS MENORES o CAMBIOS NECESARIOS) y los hallazgos por severidad, y te pregunta qué corregir. `/bowser-feature` ya pide su propia revisión; este comando es para cuando quieres una más o elegir tú qué se corrige.

---

## /bowser-close

**Para:** cerrar lo terminado y dejarlo listo para merge.

**Cuándo:** después de `/bowser-feature`, cuando probaste el resultado y está bien.

```
/bowser-close
/bowser-close al final decidimos que los mecánicos no ven precios
```

**Qué hace:**
0. `make verify`. Si algo falla, no cierra: lo resuelve (la prueba que falta, la revisión, el plan grande) o te pregunta. Nunca afloja los controles para que pase.
1. **Memoria**: actualiza solo lo que este cambio dejó viejo (requerimientos, producto, base de datos, arquitectura, decisiones, trampas, deuda). Vuelve a correr `make verify` y resuelve cada aviso de memoria.
2. **Costo**: `make cost`.
3. **Historial**: una línea en `docs/producto/historial.md` (fecha, funcionalidad, rama, tamaño, tokens, costo, vueltas de revisión, una nota) y el estado en el roadmap.
4. **Commit** de todo eso.
5. Te dice qué cambió en la memoria y el costo. El push y el merge los haces tú.

---

## /bowser-resume

**Para:** seguir algo a medias sin explicarle nada al agente.

**Cuándo:** se cortó la sesión, se reinició la máquina, cerraste OpenCode, o la conversación se hizo tan larga que conviene empezar otra.

```
/bowser-resume
```

No confía en lo que cree recordar: mira la rama y sus commits, la sección Estado del plan y lo que quedó sin commitear (y corre las pruebas para saber si está sano). Te dice qué está hecho, qué quedó a medias, qué sigue y qué decisión estaba pendiente, y te pregunta si sigue desde ahí. No descarta nada sin preguntarte.

---

## /bowser-cost

**Para:** saber cuántos tokens lleva la rama.

```
/bowser-cost
/bowser-cost todo        # todas las sesiones del proyecto
```

Te da el total y los agentes o modelos que más pesan. Ver [Costo](10-costo.md).

---

## /bowser-update

**Para:** actualizar el kit en el proyecto.

```
/bowser-update
```

Corre `bowser update --verificar`, te resume qué cambia (del CHANGELOG) y qué archivos del proyecto cambiarían, te pregunta, actualiza, commitea `chore: actualiza bowser-ai-lite a <versión>` y te recuerda cerrar y volver a abrir OpenCode.

---

## El comando `bowser`

Se usa en la terminal, en la carpeta del proyecto.

| Comando | Qué hace |
|---|---|
| `bowser init` | Instala el kit en la carpeta actual (o la que indiques). Nunca reemplaza tus archivos |
| `bowser init --skills go,react` | Instala además esas skills y las anota en `.bowser/skills` |
| `bowser init --verificar` | Dice qué haría, sin escribir nada |
| `bowser init --forzar` | Reemplaza también los archivos del kit que editaste (deja respaldo en `.bowser/respaldo/`) |
| `bowser update` | Baja la última versión del kit y actualiza el proyecto. Opciones: `--verificar`, `--version vX.Y.Z`, `--solo-kit`, `--forzar` |
| `bowser version` | La versión del kit instalado y la del proyecto |

## Comandos de make

| Comando | Qué hace | De quién es |
|---|---|---|
| `make run` | Levanta el proyecto en local | Del proyecto: lo defines tú |
| `make test` | Corre todas las pruebas | Del proyecto |
| `make lint` | Formato y revisión estática | Del proyecto |
| `make check` | Todo lo que debe pasar antes de entregar (por defecto `lint` y `test`). Lo corren el hook antes de cada push y el CI | Del proyecto |
| `make ci-setup` | Opcional: lo que el CI prepara antes de `make check` | Del proyecto |
| `make verify` | Si la rama se puede cerrar. Ver [Controles](08-controles.md#make-verify) | Del kit |
| `make cost` | Tokens y costo de la rama (`ALL=1`: de todo el proyecto) | Del kit |
| `make hooks` | Activa los hooks de git (una vez por clon) | Del kit |

Siguiente: [6. Agentes](06-agentes.md)
