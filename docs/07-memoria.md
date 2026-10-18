# 7. Memoria y documentación

[← Inicio](README.md)

La memoria del proyecto es lo que el agente necesita saber y **el código no dice**: por qué algo es así, qué hizo perder tiempo, qué se pidió, cómo son los datos. Es Markdown en git, dentro del proyecto: se revisa en los pull requests como el código, no se pierde si cambias de máquina y no depende de OpenCode.

## Qué va en cada archivo

| Pregunta | Archivo | Lo escribe | El agente lo lee cuando… |
|---|---|---|---|
| ¿Qué es, cómo se corre, qué reglas tiene? | `AGENTS.md` | Tú, `/bowser-idea`, `/bowser-discover` | Siempre, al empezar |
| ¿Qué debe hacer el sistema y para quién? | `docs/producto/requerimientos.md` | `/bowser-idea` o `/bowser-discover`; luego `/bowser-feature` y `/bowser-close` | La tarea agrega o cambia un comportamiento |
| ¿En qué orden se construye? | `docs/producto/roadmap.md` | `/bowser-idea`, `/bowser-roadmap`; `/bowser-close` actualiza el estado | Se planea o se retoma |
| ¿Qué se entregó y cuánto costó? | `docs/producto/historial.md` | `/bowser-close` | Se mide o se cotiza |
| ¿Qué existe hoy? | `docs/memoria/producto.md` | `/bowser-close`, `/bowser-discover` | Necesita saber qué funcionalidades hay |
| ¿Cómo está construido? | `docs/memoria/arquitectura.md` | `/bowser-discover`, `/bowser-close` | Va a tocar más de un módulo o no sabe dónde va algo |
| ¿Cómo son los datos? | `docs/memoria/base-de-datos.md` | `/bowser-discover`, `/bowser-close` | La tarea toca tablas, consultas o migraciones |
| ¿Por qué es así? | `docs/memoria/decisiones.md` | Quien decide, en el momento | Va a cambiar algo que parece raro |
| ¿Qué hizo perder tiempo? | `docs/memoria/trampas.md` | `/bowser-close`, `/bowser-discover` | Antes de levantar, probar o desplegar |
| ¿Cómo se escribe código aquí? | `docs/memoria/convenciones.md` | `/bowser-discover`, tú | Va a escribir código |
| ¿Qué está mal y no se arregló? | `docs/memoria/deuda.md` | Cualquier comando que la encuentre | Toca un módulo con deuda |
| ¿Qué se pidió en un cambio concreto y en qué va? | `docs/cambios/<nombre>.md` | `/bowser-feature` | Retoma ese cambio |

El agente no lee todo siempre: la tabla de `AGENTS.md` le dice cuándo leer cada archivo, para no gastar tokens en lo que la tarea no necesita.

## El formato

El formato está en `.bowser/documentacion.md` (del kit) y es el mismo para un proyecto nuevo y uno existente.

**Requisitos funcionales**: `RF-NN`, numerados y nunca reutilizados, uno por comportamiento que una persona puede comprobar. Cada uno dice quién lo usa, qué logra, su estado y de 1 a 3 criterios de aceptación:

```markdown
### RF-03 · El cliente reserva una cita
- **Quién y para qué:** un cliente reserva un horario para llevar su auto, sin llamar al taller.
- **Estado:** planeado. **Roadmap:** #3.
- **Criterios de aceptación:**
  - Dado un horario libre, cuando el cliente lo elige y confirma, entonces la cita queda reservada y el taller la ve en su agenda.
  - Dado un horario que otro cliente acaba de tomar, cuando intenta confirmarlo, entonces ve un aviso y los horarios libres.
```

El archivo también tiene visión, roles, alcance (qué incluye y qué no), restricciones, preguntas abiertas (cada una con una recomendación) y glosario.

Los estados son `planeado`, `en curso`, `existe` y `descartado`. Uno descartado se queda, tachado, con el motivo. En un proyecto existente, cada requisito descubierto dice dónde se vio (`archivo:línea`, tabla o pantalla).

**Requisitos no funcionales**: `RNF-NN`, solo si son comprobables ("responde en menos de 500 ms con 100 usuarios", no "debe ser rápido").

**Diagramas**: siempre en [Mermaid](https://mermaid.js.org), dentro del Markdown, para que el agente los pueda leer y cambiar. Cada uno con una frase que dice qué muestra, como máximo ~15 cajas y los nombres del código.

| Diagrama | Mermaid | Dónde |
|---|---|---|
| Contexto: el sistema, sus usuarios y sistemas externos | `flowchart` | `arquitectura.md` |
| Contenedores: las piezas que se despliegan | `flowchart` | `arquitectura.md` |
| Modelo de datos | `erDiagram` | `base-de-datos.md` |
| Un flujo con varias piezas | `sequenceDiagram` | `arquitectura.md` o el plan del cambio |
| Estados de algo con ciclo de vida | `stateDiagram-v2` | `arquitectura.md` o el plan del cambio |

**Decisiones**: `D-NN`, la más reciente arriba, con fecha, contexto, qué se decidió, qué se descartó y por qué, su consecuencia y quién decidió. Una decisión reemplazada se marca "reemplazada por D-NN" y no se borra. Va una entrada por cada decisión que alguien podría querer deshacer sin conocer el motivo.

**Cómo se escribe**: español claro para alguien que no estuvo en la conversación; lo que el código ya dice no se copia; un dato vive en un solo archivo y los demás lo enlazan; si un archivo pasa de ~7 000 caracteres, se resume o se parte.

## Cómo se mantiene al día

Una memoria vieja es peor que ninguna: el agente confía en ella. Por eso:

1. **Si la memoria contradice al código, manda el código**, y el documento se corrige en el mismo cambio.
2. **`/bowser-close` actualiza solo lo que el cambio dejó viejo**, en cada funcionalidad.
3. **`make verify` avisa** cuando un cambio debería haber tocado la memoria y no lo hizo: una migración sin actualizar `base-de-datos.md`, un `docker-compose` o el `Makefile` sin actualizar `AGENTS.md`, una carpeta de código nueva sin actualizar `arquitectura.md`. Son avisos, no bloquean; `/bowser-close` los resuelve o explica por qué no hace falta. Las reglas están en la sección `[memoria]` de `.bowser/verificacion` y puedes agregar las tuyas (ver [Controles](08-controles.md#bowserverificacion)).

## El plan de cada cambio

`docs/cambios/<nombre>.md` lo escribe `/bowser-feature` en los cambios normales y grandes, con el mismo nombre que la rama. Empieza con `**Tamaño:** normal` o `**Tamaño:** grande` y termina con la sección **Estado**:

```markdown
## Estado
- Hecho: tabla `citas` con su migración y prueba; API para crear y listar.
- Sigue: formulario de reserva.
- Por decidir: ¿un mecánico ve las citas de otros? (la persona dijo que sí para el dueño)
```

El Estado se commitea con cada paso. Es lo que lee `/bowser-resume` después de un corte y lo que muestra `/bowser-roadmap` de lo que está en curso.

Siguiente: [8. Controles](08-controles.md)
