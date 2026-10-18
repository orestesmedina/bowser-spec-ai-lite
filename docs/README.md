# Documentación de bowser-ai-lite

bowser-ai-lite es un kit para construir software con un agente de IA en [OpenCode](https://opencode.ai) sin caer en el *vibecoding*: el agente trabaja con un método, con una memoria del proyecto y con controles que no dependen de que obedezca.

Esta documentación está pensada para alguien que nunca usó el kit. Si tienes cinco minutos, lee [Qué es y cómo piensa](01-que-es.md) y [Elegir el comando](03-elegir-el-comando.md).

## Empezar

| Página | Para… |
|---|---|
| [1. Qué es y cómo piensa](01-que-es.md) | Entender las ideas del kit antes de usarlo |
| [2. Instalar](02-instalar.md) | Dejarlo listo en tu máquina y en un proyecto (nuevo, existente o con el kit anterior) |
| [3. Elegir el comando](03-elegir-el-comando.md) | Saber qué escribir en cada situación |
| [4. Un día de trabajo](04-un-dia-de-trabajo.md) | Ver el ciclo completo con un ejemplo, de la idea al merge |

## Referencia

| Página | Para… |
|---|---|
| [5. Comandos](05-comandos.md) | Qué hace cada comando paso a paso, qué te pregunta y qué deja escrito |
| [6. Agentes](06-agentes.md) | Quién es el constructor, el revisor y el explorador, y qué pueden hacer |
| [7. Memoria y documentación](07-memoria.md) | Qué va en cada archivo de `docs/`, quién lo escribe y cómo se mantiene al día |
| [8. Controles](08-controles.md) | Hooks de git, `make verify` y CI: qué revisa cada uno y cómo se ajusta |
| [9. Skills de tecnología](09-skills.md) | Los estándares por tecnología y cómo se instalan |
| [10. Costo](10-costo.md) | Cuántos tokens gasta cada funcionalidad y cómo leerlo |
| [11. Archivos que instala](11-archivos.md) | Cada archivo del kit en tu proyecto, de quién es y qué pasa al actualizar |
| [12. Problemas frecuentes](12-problemas.md) | Qué hacer cuando algo no aparece, no pasa o se corta |
| [13. Trabajar en el kit](13-trabajar-en-el-kit.md) | Pruebas del kit, CI y cómo publicar una versión |

## En una línea por comando

| Comando | Cuándo |
|---|---|
| `/bowser-idea` | Tienes una idea y ninguna línea de código |
| `/bowser-discover` | Tienes un proyecto que funciona y nadie lo documentó |
| `/bowser-roadmap` | Vuelves al proyecto y no recuerdas en qué ibas, o quieres cambiar el plan |
| `/bowser-feature` | Quieres construir, corregir o cambiar algo |
| `/bowser-review` | Quieres una segunda opinión sobre la rama antes de entregar |
| `/bowser-close` | Lo construido está bien y quieres cerrarlo |
| `/bowser-resume` | Se cortó la sesión, o sigues algo a medias en una sesión nueva |
| `/bowser-cost` | Quieres saber cuánto lleva gastado la rama |
| `/bowser-update` | Hay una versión nueva del kit |
