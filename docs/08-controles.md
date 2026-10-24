# 8. Controles

[← Inicio](README.md)

Las instrucciones de un agente se pueden ignorar; un hook de git, no. Por eso lo importante no depende de que el agente obedezca: lo comprueban programas, igual para el agente que para una persona.

| Cuándo | Control | Qué frena |
|---|---|---|
| Cada commit | Hook `pre-commit` | Secretos y cambios a archivos inmutables |
| Cada commit | Hook `commit-msg` | Mensajes que no siguen Conventional Commits |
| Cada push | Hook `pre-push` | Lo que no pasa `make check` |
| Al cerrar una rama | `make verify` | Código sin pruebas, cambios riesgosos sin plan grande, ramas sin revisión |
| Cada pull request y push a main | CI (`.github/workflows/bowser.yml`) | Secretos, `make check` y las pruebas y el tamaño de la rama |

Ninguno se salta con `--no-verify`: el agente tiene prohibido hacerlo, y aunque una persona lo haga en su máquina, el CI vuelve a revisar.

## Hooks de git

Están en `.githooks/` y el instalador los activa (`git config core.hooksPath .githooks`). **En cada clon nuevo del proyecto hay que activarlos una vez** con `make hooks`: git no guarda esa configuración en el repositorio.

**pre-commit**
- No deja commitear `.env`, `.env.*` (salvo `.env.example` y `.env.sample`), `*.pem`, `*.key`, `*.p12`, `*.pfx` ni nada en `secrets/`.
- Si tienes [gitleaks](https://github.com/gitleaks/gitleaks) instalado, busca secretos en lo que vas a commitear.
- No deja modificar, renombrar ni borrar un archivo que esté en git y coincida con `.bowser/inmutables` (por ejemplo, una migración ya aplicada). Para cambiar algo así, se crea un archivo nuevo.

**commit-msg**: el mensaje empieza con un tipo de [Conventional Commits](https://www.conventionalcommits.org/es/): `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, `ci`, `perf`, `build`, `style` o `revert`, con ámbito opcional: `feat(citas): reserva desde el celular`. Se aceptan los merges y reverts que genera git.

**pre-push**: corre `make check`. Si el `Makefile` no tiene `check`, o falla, el push no sale. Con `test` y `lint` todavía sin definir (como vienen en la plantilla), `make check` avisa y pasa: un proyecto que es solo documentos se puede subir.

## make verify

Dice si la rama actual se puede cerrar. Lo corren `/bowser-feature` al entregar y `/bowser-close` antes de cerrar, y puedes correrlo tú en cualquier momento. Compara la rama contra `main` (o `master`; otra con `--base`).

| Comprueba | Falla si… | Cómo se resuelve |
|---|---|---|
| `make check` | Falla | Arreglar lo que falla |
| Comandos del `Makefile` | La rama cambia código y `test` o `lint` siguen sin definir (sin código, solo avisa). También en el CI | Definirlos con los comandos reales del proyecto |
| Pruebas | La rama cambia código y ningún archivo de pruebas | Agregar la prueba. Si de verdad no aplica, un commit con la línea `Sin-pruebas: <motivo>` (queda como aviso, a la vista del revisor) |
| Tamaño | Toca un archivo riesgoso y no hay plan en `docs/cambios/<nombre>.md` (la rama sin `feat/` o `fix/`) que diga «Tamaño: grande», commiteado **antes** del primer cambio riesgoso | Escribir el plan grande y aprobarlo. Si ya se programó, rehacer la rama con el plan primero |
| Revisión | El agente revisor no revisó la rama (lo busca en las sesiones de OpenCode desde que empezó la rama) | `/bowser-review`. Si hubo cambios de código después de la última revisión, solo avisa |
| Memoria | Nunca falla: avisa | Ver [Memoria](07-memoria.md#cómo-se-mantiene-al-día) |

Un ejemplo de `Sin-pruebas`, para un cambio que solo toca configuración de despliegue:

```bash
git commit -m "chore: sube el límite de memoria del contenedor" -m "Sin-pruebas: configuración de despliegue, sin lógica"
```

| Opción | Para… |
|---|---|
| `--base origin/develop` | Comparar contra otra rama |
| `--sin-check` | No correr `make check` (si lo acabas de correr) |
| `--ci` | Lo que usa el CI: sin `make check`, sin revisión ni memoria (no hay sesiones de OpenCode). Sí comprueba que `test` y `lint` estén definidos si la rama trae código |

## El CI

`.github/workflows/bowser.yml` corre en GitHub Actions en cada pull request y en cada push a `main` o `master`:

| Trabajo | Qué hace |
|---|---|
| Búsqueda de secretos | gitleaks sobre los commits del push o del pull request |
| make check | Instala Go, Node o PHP si el proyecto los usa (por `go.mod`, `package.json`, `composer.json`), en las versiones de `.bowser/versiones`; corre `make ci-setup` si existe y luego `make check` |
| Pruebas y tamaño de la rama | Solo en pull requests: `make verify` en modo CI (pruebas y tamaño) |

**Las versiones van en `.bowser/versiones`**, que es del proyecto, no en el workflow. Pon las mismas que corren en local y en producción, para que el CI pruebe lo mismo:

```
go=1.27
php=8.4
node=22
```

Sin valor, Go toma la de `go.mod`, PHP la última y Node la LTS. No edites el workflow para fijarlas: el workflow es del kit y, si lo editas, cada mejora que traiga el kit tendrás que pasarla a mano.

El workflow solo pide permisos de lectura (`contents` y `pull-requests`, que gitleaks necesita para listar los commits del pull request).

Si las pruebas necesitan algo más (dependencias, una base de datos), ponlo en el objetivo `ci-setup` del `Makefile`. Si necesitan un servicio (PostgreSQL, MySQL), agrégalo como `services:` del trabajo "make check" en el workflow. Al editarlo, el archivo pasa a ser tuyo: `bowser update` no lo toca y, cuando el kit traiga cambios en él, te muestra cómo verlos (`diff -u`) para que los pases a mano.

Para que el CI frene un merge, actívalo en GitHub: *Settings → Branches → Branch protection rules* y marca los tres trabajos como obligatorios.

## .bowser/verificacion

Es del proyecto: dice qué cuenta como prueba, qué es riesgoso y qué no es código. Un patrón por línea, estilo glob (`*` también cruza carpetas; un patrón sin carpeta vale para el nombre del archivo).

| Sección | Para qué | Por defecto |
|---|---|---|
| `[pruebas]` | Archivos que cuentan como pruebas | `*_test.go`, `*.test.*`, `*.spec.*`, `test_*.py`, `*_test.py`, `*Test.php`, `tests/`, `test/`, `__tests__/`, `e2e/` |
| `[riesgo]` | Tocarlos hace el cambio grande | Migraciones, `*.sql`, y nombres con `auth`, `permis`, `login`, `password`, `contrasen`, `pago`, `payment`; también `.bowser/inmutables` |
| `[no-codigo]` | No cuentan como código (no exigen pruebas) | `*.md`, `docs/`, `.bowser/`, `.opencode/`, `.githooks/`, `.github/`, archivos de bloqueo de dependencias |
| `[memoria]` | `patrón -> archivo`: si la rama toca el patrón y no ese archivo, `make verify` avisa | Migraciones y SQL → `base-de-datos.md`; `docker-compose`, `compose.y*` y `Makefile` → `AGENTS.md` |

Ajústalo a tu proyecto (por ejemplo, agrega `*Spec.php` a pruebas o `facturacion/*` a riesgo), pero **nunca para que una rama pase**: eso se decide con una persona. El agente tiene prohibido cambiarlo, salvo `/bowser-discover`, que lo ajusta una vez y te muestra el cambio.

## .bowser/inmutables

Archivos que, una vez en git, no se modifican, renombran ni borran. Típicamente, las migraciones ya aplicadas:

```
backend/migrations/*.sql
database/*.sql
```

Lo comprueba el hook `pre-commit`. Además, tocar este archivo cuenta como cambio riesgoso.

## Los principios

`.bowser/principios.md` tiene las reglas que valen en cualquier proyecto: seguridad (consultas con parámetros, validación en el servidor, escape, contraseñas con bcrypt o argon2, secretos fuera del código, autorización en el servidor, dependencias sin vulnerabilidades graves, datos personales mínimos), calidad (cada cambio con su prueba, nada con pruebas fallando, los controles no se aflojan), datos (cambios de esquema versionados y reversibles, nada de borrar en masa sin pedirlo) y personas (push, merge y despliegue los decide una persona; lo ambiguo se pregunta; lo que está fuera de la tarea se anota). El constructor los lee al empezar y el revisor los revisa. `AGENTS.md` puede agregar o endurecer reglas, nunca quitar estas.

Siguiente: [9. Skills de tecnología](09-skills.md)
