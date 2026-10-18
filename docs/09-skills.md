# 9. Skills de tecnología

[← Inicio](README.md)

Una skill es un archivo con los estándares de una tecnología (cómo se nombra, cómo se manejan errores, qué evitar por seguridad). OpenCode la carga **solo cuando el agente trabaja con esa tecnología**, así que no gasta tokens en las demás. El constructor la carga antes de escribir código y el revisor la usa para revisar.

## Las que trae el kit

| Skill | Para | Basada en |
|---|---|---|
| `go` | Servicios en Go (archivos `.go`) | Effective Go, Go Code Review Comments, guías de go.dev |
| `react` | Interfaces en React con TypeScript (`.tsx`, `.jsx`) | react.dev: Reglas de React, estado, efectos |
| `postgres` | Tablas, índices, consultas, migraciones y funciones en PostgreSQL | El manual y la lista "Don't Do This" de la wiki de PostgreSQL |
| `php` | PHP sin framework (`.php`) | PSR-1, PSR-4, PER Coding Style y el manual de PHP |
| `mysql` | Tablas, índices, consultas y procedimientos en MySQL | El manual de referencia de MySQL |
| `web` | HTML, CSS y JavaScript sin framework ni compilación | El estándar HTML, WCAG, MDN y OWASP |

Vienen del kit anterior y todavía no se han probado en un proyecto real con este kit.

## Instalar y quitar

Cada proyecto instala solo las suyas. Quedan anotadas en `.bowser/skills`, una por línea.

```bash
bowser init --skills go,react,postgres    # agrega estas
```

Si no pones `--skills`, el instalador mira el proyecto y te sugiere las que parecen servirle. Para quitar una, bórrala de `.bowser/skills` y corre `bowser update` (o `bowser init`): el instalador retira su archivo. Después, cierra y vuelve a abrir OpenCode.

## Qué manda si chocan

1. `.bowser/principios.md` (seguridad, calidad, datos) manda siempre.
2. `docs/memoria/convenciones.md` (cómo se hace en **este** proyecto) manda sobre la skill, salvo en seguridad. Si tu proyecto nombra las tablas en singular y la skill dice plural, se sigue el proyecto.
3. La skill, para todo lo que el proyecto no decidió.

## Skills propias

Puedes agregar las tuyas en `.opencode/skills/<nombre>/SKILL.md`, con el formato de [skills de OpenCode](https://opencode.ai/docs/skills/): un encabezado con `name` y `description` (la descripción le dice al agente cuándo cargarla). El instalador no las toca, porque no son del kit.

Siguiente: [10. Costo](10-costo.md)
