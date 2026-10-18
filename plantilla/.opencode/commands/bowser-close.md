---
description: "Cierra la funcionalidad actual: memoria al día, historial y costo registrados, listo para merge."
agent: constructor
---
<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit. -->

Notas de la persona (puede venir vacío): $ARGUMENTS

0. **Verificación.** Ejecuta `make verify`. Si marca algo con ✗, **no cierres**: resuélvelo (la prueba que falta, la revisión con `@revisor`, el plan de tamaño grande) y vuelve a correrlo. Nunca cambies `.bowser/verificacion`, los hooks ni el CI para que pase. Si no puedes resolverlo, muestra la salida a la persona y pregúntale qué hacer.
1. **Memoria.** Revisa qué dejó vieja este cambio y actualiza solo eso en `docs/memoria/`:
   - `docs/producto/requerimientos.md`: los requisitos de este cambio pasan a `existe`; los nuevos se agregan con sus criterios.
   - `producto.md`: la funcionalidad nueva o lo que cambió de una existente.
   - `base-de-datos.md`: tablas, columnas, procedimientos o índices nuevos o cambiados (léelos del esquema real).
   - `arquitectura.md`: piezas o flujos nuevos, con sus diagramas (si el plan los traía, se pasan aquí).
   - `decisiones.md`: lo que se decidió en la conversación y alguien podría querer deshacer sin saber el motivo.
   - `trampas.md`: lo que hizo perder tiempo en esta sesión.
   - `deuda.md`: lo que se encontró y no se arregló.
   Sigue `.bowser/documentacion.md`. No repitas lo que el código ya dice. Si un archivo pasa de ~7 000 caracteres, resume o pártelo.
   Después corre `make verify` otra vez: cada aviso `⚠ memoria:` se resuelve actualizando ese archivo, o se explica a la persona por qué no hace falta.
2. **Costo.** Ejecuta `make cost` y toma el total de tokens y el costo equivalente.
3. **Historial.** Agrega una línea a `docs/producto/historial.md`: fecha, funcionalidad, rama, tamaño, tokens, costo, vueltas de revisión y una nota breve (qué costó más, o qué falló). Actualiza su estado en `docs/producto/roadmap.md`.
4. **Commit** de todo esto: `docs: memoria e historial de <funcionalidad>`.
5. Muestra a la persona, en pocas líneas, qué cambiaste en la memoria y el costo. Recuérdale que el push y el merge los hace ella (o pídele permiso si quiere que lo hagas tú).
