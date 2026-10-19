# Estándar de documentación

<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. Dice CÓMO se escribe la documentación del
     proyecto; el contenido vive en docs/. Léelo antes de crear o cambiar un archivo de docs/producto o docs/memoria. -->

Vale igual para un proyecto nuevo y para uno existente. Lo único que cambia es el origen: en uno nuevo los
documentos se escriben desde la idea, antes del código; en uno existente se escriben leyendo el código y la base de
datos, y describen lo que ya hay. Desde ahí, cada funcionalidad parte de ellos y los deja al día al cerrar.

## Qué va en cada archivo

| Pregunta | Archivo | Lo escribe |
|---|---|---|
| ¿Qué debe hacer el sistema y para quién? | `docs/producto/requerimientos.md` | `/bowser-idea` o `/bowser-discover`; luego `/bowser-feature` y `/bowser-close` |
| ¿En qué orden se construye? | `docs/producto/roadmap.md` | `/bowser-idea` o `/bowser-roadmap`; `/bowser-close` actualiza el estado |
| ¿Qué existe hoy? | `docs/memoria/producto.md` | `/bowser-close` |
| ¿Cómo está construido? (piezas, flujos, diagramas) | `docs/memoria/arquitectura.md` | `/bowser-discover`; `/bowser-close` |
| ¿Para qué sirve cada módulo y quién puede usar a quién? | `docs/memoria/modulos.md` | `/bowser-idea` (diseño) o `/bowser-discover`; `/bowser-close` |
| ¿Cómo se escribe código aquí? | `docs/memoria/convenciones.md` | `/bowser-idea` o `/bowser-discover`, con `.bowser/estandares.md`; quien decide |
| ¿Cómo son los datos? | `docs/memoria/base-de-datos.md` | `/bowser-idea` (diseño) o `/bowser-discover`; `/bowser-close` |
| ¿Por qué es así? | `docs/memoria/decisiones.md` | Quien decide, en el momento |
| ¿Qué se pidió en un cambio concreto? | `docs/cambios/<nombre>.md` | `/bowser-feature` |

Un dato vive en un solo archivo; los demás lo enlazan. Si la documentación contradice al código, manda el código y
el documento se corrige en el mismo cambio.

## Requisitos

- **Funcionales:** `RF-NN`, numerados y nunca reutilizados. Uno por comportamiento que una persona puede comprobar.
  Cada uno con quién lo usa, qué logra, su estado y de 1 a 3 criterios de aceptación en forma *Dado / Cuando / Entonces*.
- **Estado:** `planeado`, `en curso`, `existe` o `descartado`. Uno descartado se queda, tachado, con el motivo.
- **No funcionales:** `RNF-NN`, solo los que tienen un número o una regla comprobable ("responde en menos de 500 ms
  con 100 usuarios", no "debe ser rápido"). Los principios del kit no se repiten aquí.
- **En un proyecto existente**, cada requisito descubierto lleva dónde se vio (`archivo:línea`, tabla o pantalla) y
  estado `existe`. Lo que parece un error o no tiene sentido no se convierte en requisito: va a `deuda.md` o a
  "Preguntas abiertas".
- Lo que no se sabe va a **Preguntas abiertas**, con la recomendación de quien pregunta. No se inventa.

## Diagramas

- Siempre en **Mermaid**, dentro del Markdown. Nada de imágenes ni de archivos de otras herramientas: el agente
  tiene que poder leerlos y cambiarlos.
- Cada diagrama tiene una frase encima que dice qué muestra, y como máximo ~15 cajas. Si no cabe, se parte.
- Los nombres de las cajas son los del código (carpeta, servicio, tabla), para que se puedan buscar.

| Diagrama | Mermaid | Dónde | Cuándo |
|---|---|---|---|
| Contexto: el sistema, sus usuarios y los sistemas externos | `flowchart` | `arquitectura.md` | Siempre |
| Contenedores: las piezas que se despliegan y cómo se hablan | `flowchart` | `arquitectura.md` | Siempre |
| Modelo de datos | `erDiagram` | `base-de-datos.md` | Si hay base de datos |
| Secuencia de un flujo clave | `sequenceDiagram` | `arquitectura.md` o el cambio | Flujos con varias piezas, pagos o permisos |
| Estados de una entidad | `stateDiagram-v2` | `arquitectura.md` o el cambio | Pedidos, solicitudes, cualquier cosa con ciclo de vida |
| Quién usa a quién entre módulos | `flowchart` | `modulos.md` | Si hay más de un módulo |

Un cambio grande que agrega piezas, tablas o un flujo nuevo trae sus diagramas en `docs/cambios/<nombre>.md`, y
`/bowser-close` los pasa a `arquitectura.md` o `base-de-datos.md`.

## Decisiones

Una entrada por decisión que alguien podría querer deshacer sin conocer el motivo: `D-NN`, fecha, título, contexto,
qué se decidió, qué se descartó y por qué, y su consecuencia. La más reciente arriba. Si una decisión reemplaza a
otra, la vieja se marca "reemplazada por D-NN" y no se borra.

## Cómo se escribe

- En español claro, para alguien que no estuvo en la conversación. Frases cortas.
- Lo que el código ya dice (nombres de funciones, cada columna de cada tabla) no se copia: se enlaza.
- Si un archivo pasa de ~7 000 caracteres, se resume o se parte por parte del sistema.
