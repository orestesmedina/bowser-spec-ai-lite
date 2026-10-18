# 10. Costo

[← Inicio](README.md)

Cada respuesta de un agente gasta tokens. El kit los cuenta leyendo las sesiones de OpenCode guardadas en tu máquina, sin servicios externos.

```bash
make cost            # la rama actual
make cost ALL=1      # todas las sesiones del proyecto
```

En OpenCode: `/bowser-cost` (o `/bowser-cost todo`).

```
Costo de IA · rama feat/agenda · 3 sesiones (incluye subagentes)

  Agente         Modelo                      Resp.   Entrada    Salida     Caché  Costo eq.
  constructor    deepseek-v4.1-flash            84     2.1 M     95 k     18.4 M      $1.92
  revisor        mimo-v2.6-pro                   6     310 k     12 k      1.1 M      $0.41
  explorador     glm-5.3-flash                  11     420 k     21 k      2.0 M      $0.12

  Total: 24.5 M tokens · $2.45 equivalente · 101 respuestas
  (Con OpenCode Go el gasto real es el % de su consola; los tokens son la medida para comparar.)
```

*(Los números son de ejemplo.)*

## Cómo leerlo

- **Rama actual**: cuenta las sesiones de este proyecto desde que se creó la rama. En la rama principal cuenta todas y avisa.
- **Costo equivalente**: lo que costaría a precio de API, según calcula OpenCode. Con un plan de suscripción como OpenCode Go, el gasto real es el porcentaje que muestra su consola. **Los tokens sí son reales** y son la medida que conviene comparar entre funcionalidades.
- **Caché**: tokens que el modelo reutiliza de respuestas anteriores. Son mucho más baratos, pero crecen con cada respuesta de una conversación larga. Por eso conviene una sesión por funcionalidad.

## Dónde queda

`/bowser-close` anota los tokens y el costo de cada funcionalidad en `docs/producto/historial.md`, junto con su tamaño y las vueltas de revisión. Con el tiempo, ese historial sirve para saber cuánto cuesta un trabajo parecido antes de empezarlo.

## Opciones

```bash
python3 .bowser/costo.py --desde 2026-10-01   # desde una fecha
python3 .bowser/costo.py --json               # para procesarlo con otro programa
```

## Gastar menos

- Una sesión de OpenCode por funcionalidad, y `/bowser-resume` en una nueva si la conversación se alarga.
- Pedir a `@explorador` que lea zonas grandes de código: usa un modelo más barato y el constructor solo lee su resumen.
- Mantener la memoria corta: el agente lee solo lo que la tarea necesita, pero lo que lee lo paga.
- Usar el tamaño correcto: un cambio pequeño no necesita plan.

Siguiente: [11. Archivos que instala](11-archivos.md)
