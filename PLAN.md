# Plan del kit nuevo

Fecha: 2026-10-14 · Estado: propuesta para discutir; no se ha construido nada. Viene de la auditoría (`AUDITORIA.md`) y de la conversación con Orestes de ese día.

## 1. Qué tiene que lograr

Una persona con el kit y OpenCode puede:

1. **Partir de una idea** y llegar a un producto: darle forma, convertirla en tareas, código, pruebas y despliegue.
2. **Partir de un proyecto existente**, entenderlo completo (código, módulos, base de datos) mediante ingeniería inversa y, desde ahí, agregar funcionalidades, modificarlas o reconstruir módulos enteros.

En los dos casos el agente trabaja con una **memoria del proyecto** que sabe lo que el código no dice.

## 2. Principios (lo que aprendimos del kit anterior)

| Principio | En la práctica |
|---|---|
| Un agente fuerte hace el trabajo | El agente principal construye de punta a punta con el mejor modelo disponible. Los subagentes solo exploran en paralelo o revisan con contexto limpio. |
| Ceremonia según el tamaño | Un cambio pequeño no lleva spec. Una funcionalidad grande sí. |
| Evidencia antes que documentos | La persona aprueba viendo pruebas en verde y la app funcionando, no leyendo planes largos. |
| Controles en el código, no en el prompt | Lo que un hook o el CI impide no se repite en las instrucciones. |
| El agente puede verificar su trabajo | Corre pruebas, linters y la app sin pedir permiso. Push, borrado de datos y producción sí piden permiso. |
| Memoria pequeña y curada | Solo lo que el código no dice y seguirá siendo cierto. Una memoria vieja es peor que ninguna. |
| Una sola herramienta | OpenCode. La memoria es Markdown en git, así que no queda atada a ella. |
| Construir con proyectos reales | Nada entra al kit sin haberse usado en un proyecto (regla de tres). |

## 3. Las piezas

```
proyecto/
├── AGENTS.md                 ← instrucciones cortas (< ~100 líneas); OpenCode lo lee solo
├── Makefile                  ← make run / test / lint del proyecto (lo que el agente usa)
├── docs/
│   ├── producto/
│   │   ├── idea.md           ← solo en proyectos que nacen de una idea
│   │   └── roadmap.md        ← funcionalidades y su estado
│   └── memoria/
│       ├── producto.md       ← mapa: qué funcionalidades existen y qué hace cada una
│       ├── arquitectura.md   ← módulos, cómo se conectan, diagrama Mermaid
│       ├── base-de-datos.md  ← generado del esquema real: tablas, relaciones, procedimientos, diagrama
│       ├── decisiones.md     ← una entrada por decisión, con su motivo y fecha
│       ├── trampas.md        ← lo que hace perder tiempo (versiones raras, pruebas que vacían tablas…)
│       ├── convenciones.md   ← cómo se escribe código aquí (sale de leer el código)
│       └── deuda.md          ← deuda técnica y de seguridad conocida
├── .opencode/
│   ├── agents/revisor.md     ← subagente de revisión, solo lectura
│   └── commands/             ← /idea /roadmap /descubrir /feature /revisar /cerrar
├── .githooks/                ← secretos, Conventional Commits, archivos inmutables (del kit actual)
└── .github/workflows/ci.yml  ← del proyecto
```

Reglas de la memoria:
- Cada archivo empieza con una línea que dice cuándo leerlo. `AGENTS.md` los lista y el agente lee solo los que necesita para la tarea.
- Cada archivo, idealmente por debajo de ~7 000 caracteres. Si crece, se parte por tema.
- La memoria se actualiza en el mismo PR que el cambio que la vuelve vieja, y la aprueba la persona junto con el código.
- Antes de fiarse de un dato de la memoria, el agente lo contrasta con el código.

### Agentes

| Agente | Qué hace | Modelo |
|---|---|---|
| Principal | Entrevista, planea, escribe código y pruebas, corrige, abre el PR | El mejor que tengas |
| `revisor` (subagente) | Revisa el diff contra el pedido, la seguridad y las convenciones; no edita | Otro modelo capaz, distinto del principal |
| `explorador` (subagente, opcional) | Lee una zona del código y devuelve un resumen; se usa en paralelo en `/descubrir` | Uno barato y rápido sirve |

Los 11 roles del kit anterior pasan a ser **listas de verificación** que el agente principal o el revisor cargan cuando hacen falta: seguridad, UX, base de datos, despliegue.

## 4. Puerta A: tengo una idea

| Paso | Comando | Qué pasa | Qué deja | Persona |
|---|---|---|---|---|
| 1 | `/idea` | El agente te entrevista: para quién es, qué problema resuelve, qué es imprescindible, qué queda fuera, restricciones (presupuesto, hosting, plazos) | `docs/producto/idea.md` (1–2 páginas) | Corriges y confirmas |
| 2 | `/roadmap` | Propone el stack con sus motivos, y parte la primera versión en funcionalidades pequeñas, independientes y en orden | `roadmap.md`, `decisiones.md` | Eliges orden y alcance |
| 3 | `/feature` (la primera) | **Base mínima que funciona:** la app levanta, tiene una prueba, CI en verde y se puede desplegar. Se escribe `AGENTS.md`, el `Makefile` y la memoria inicial | Proyecto que corre | Lo ves funcionando |
| 4 | `/feature` (las siguientes) | Ciclo de la sección 6 | Código, pruebas, PR | Apruebas el PR |

El momento en que una persona que no programa puede juzgar es el paso 3 en adelante: ve algo que funciona.

## 5. Puerta B: tengo un proyecto existente

| Paso | Comando | Qué pasa | Qué deja | Persona |
|---|---|---|---|---|
| 1 | `/descubrir` (pasada 1: inventario) | Detecta lenguajes, frameworks, versiones, carpetas, código de terceros, cómo se ejecuta | `arquitectura.md` (borrador), `trampas.md` | — |
| 2 | `/descubrir` (pasada 2: en paralelo) | Un explorador por módulo: qué hace, de qué depende, sus puntos de entrada | `arquitectura.md`, `producto.md` | — |
| 3 | `/descubrir` (pasada 3: datos) | Lee el esquema real (el script SQL o la base viva): tablas, relaciones, índices, procedimientos, quién usa cada uno. **Se genera del esquema, no se redacta de memoria** | `base-de-datos.md` con diagrama | — |
| 4 | `/descubrir` (pasada 4: convenciones y deuda) | Lo que ya hace `/bowser-conventions`, más la deuda de seguridad | `convenciones.md`, `deuda.md` | — |
| 5 | Prueba de entendimiento | El agente **levanta el sistema en local** (por ejemplo, Docker con la versión real de PHP y MySQL) y te explica un flujo clave paso a paso | Entorno local que corre, `AGENTS.md` | Confirmas o corriges |
| 6 | Red de seguridad | Antes de tocar un módulo, escribe **pruebas de caracterización**: fijan cómo se comporta hoy, aunque sea raro | Pruebas del módulo | — |
| 7a | `/feature` | Funcionalidad nueva o cambio: ciclo de la sección 6 | PR | Apruebas el PR |
| 7b | `/feature` (tamaño grande) | **Reconstruir un módulo:** se rehace por dentro sin cambiar cómo se conecta con el resto; las pruebas del paso 6 avisan si algo cambió. Se reemplaza por partes, no todo de golpe | PRs por partes | Apruebas cada PR |

Lo que un proyecto viejo suele no tener (git, pruebas, entorno local) se trata como parte del descubrimiento, no como un requisito para empezar.

## 6. El ciclo de una funcionalidad (`/feature`)

1. **Tamaño.** El agente propone uno y tú lo confirmas:
   - **Pequeño** (bug, texto, ajuste): directo al código.
   - **Normal**: un plan de una página en el PR (qué se hace, qué archivos, qué datos cambian, cómo se prueba).
   - **Grande o riesgoso** (datos de clientes, pagos, permisos, reconstruir un módulo): spec y plan, que apruebas antes de empezar. Aquí puede usarse Spec Kit.
2. **Construir.** El agente principal lee la memoria que hace falta, escribe pruebas y código, y corre `make test` y `make lint` todas las veces que necesite.
3. **Evidencia.** Pruebas en verde y, si hay interfaz, la app levantada con capturas del flujo.
4. **`/revisar`.** El revisor, con contexto limpio, revisa el diff. Los hallazgos bloqueantes los corrige el principal (máximo 2 vueltas; si no, te pregunta).
5. **PR.** Descripción con qué cambió, evidencia, costo de IA y propuesta de cambios a la memoria.
6. **`/cerrar`.** Al aprobarse: memoria actualizada, roadmap al día y costo registrado.

Una rama y un PR por funcionalidad. El estado de "por dónde vamos" es la rama, el PR y una nota corta en el PR, no un `estado.md` aparte.

## 7. Qué se trae del kit actual

| Se conserva | Se adapta | Se retira |
|---|---|---|
| Hooks de git (secretos, Conventional Commits, inmutables) | `/bowser-conventions` → pasada 4 de `/descubrir` | 11 roles como agentes |
| gitleaks y el workflow pequeño de controles | `make costs` → costo por funcionalidad aceptada | 9 fases y `estado.md` |
| Principios de seguridad de la constitución | Skills del catálogo → listas de verificación por tecnología, cargadas bajo demanda | Generador para tres herramientas |
| `make costs` (OpenCode) | Plantillas de idea y roadmap | Perfil con verbos (lo reemplaza el `Makefile` del proyecto) |
| Documentación en español | | Aprobaciones con frase exacta |

## 8. Cómo construirlo (orden)

| Fase | Qué | Hecho cuando |
|---|---|---|
| 0 | Repositorio nuevo y limpio; el kit actual queda congelado como referencia | Existe el repositorio, con `AGENTS.md` de plantilla y los hooks |
| 1 | Ciclo `/feature`, `/revisar`, `/cerrar` y la estructura de memoria | 3 funcionalidades pequeñas hechas en `simiente-santa-webside`, con costo, tiempo y retrabajo medidos y comparados con los 115 M tokens de la primera |
| 2 | Puerta B: `/descubrir` | p2p Controller descubierto (memoria completa, entorno Docker que corre, un flujo explicado y confirmado por Orestes) y un cambio real hecho con pruebas de caracterización |
| 3 | Puerta A: `/idea` y `/roadmap` | Una idea nueva llega a su base mínima desplegada |
| 4 | Documentación para otros e instalación simple | Alguien de fuera instala el kit y hace una funcionalidad sin ayuda |
| Después | La capa de negocio (cotizar, reportar al cliente, entregar) | Cuando haya proyectos de clientes reales con el kit |

Va primero la fase 1 (el ciclo) porque las dos puertas dependen de ella, y porque `simiente-santa-webside` ya tiene entorno. La puerta B va antes que la A porque ya hay un proyecto real esperando (p2p) y es donde el kit anterior tuvo su mejor resultado (`/bowser-conventions`).

## 9. Cómo sabremos que funciona

- **Costo por funcionalidad aceptada** (no por token) y su tendencia.
- **Tiempo de idea a PR mergeado.**
- **Minutos de Orestes por funcionalidad** (leer, aprobar, corregir).
- **PRs que pasan la revisión a la primera.**
- **Memoria útil:** cuántas veces el agente se equivocó por no saber algo que estaba (o debía estar) en la memoria.

## 10. Decisiones abiertas

| Decisión | Recomendación |
|---|---|
| Modelo del agente principal en OpenCode Go | El de mejor calidad de código, aunque gaste la ventana más rápido; probar dos y comparar con las métricas de la sección 9 |
| Repositorio nuevo o rama del actual | Repositorio nuevo |
| Nombre (sigue "bowser") | Sin cambio por ahora |
| Si Spec Kit se mantiene para funcionalidades grandes | Sí, solo ahí; revisarlo después de la fase 1 |
| Cómo entra el kit a un proyecto (submódulo como hoy, o copia simple) | Copia simple con un script de actualización; el submódulo con manifiesto agrega complejidad que hoy no se necesita |

## 11. Riesgos

- **Una persona que no programa aprobando cambios riesgosos.** Se mitiga con evidencia (app funcionando) y con el revisor, pero no se elimina: en pagos, datos personales y seguridad conviene una segunda persona técnica.
- **Ingeniería inversa equivocada.** El agente puede describir mal un módulo. Por eso existe el paso 5 (levantarlo y explicar un flujo) y las pruebas de caracterización antes de cambiar nada.
- **Volver a construir el kit en vez de los productos.** La regla: ninguna pieza nueva sin haberla necesitado tres veces en un proyecto real.
