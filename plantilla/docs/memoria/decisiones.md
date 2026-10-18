# Decisiones

Cuándo leerlo: antes de cambiar algo que parece raro o mejorable. Puede tener un motivo.

<!-- Una entrada por decisión que alguien podría querer deshacer sin conocer el motivo. La más reciente arriba.
     Si una decisión reemplaza a otra, la vieja se marca "Reemplazada por D-NN" y no se borra.
     Formato en .bowser/documentacion.md. -->

### D-01 · <AAAA-MM-DD> · <Todas las escrituras pasan por procedimientos almacenados>
- **Contexto:** <el cliente audita la base de datos y exige que la lógica de escritura viva ahí.>
- **Decisión:** <la aplicación no hace INSERT ni UPDATE directos; llama a un procedimiento.>
- **Descartado:** <escribir desde el ORM, porque la auditoría no lo acepta.>
- **Consecuencia:** <cada escritura nueva necesita su procedimiento y su migración.>
- **Decidió:** <nombre>.
