# bowser-ai-lite · Comandos del kit. Se reemplaza al actualizar: lo del proyecto va en el Makefile.
# El Makefile del proyecto lo incluye con: -include bowser.mk

.PHONY: cost verify hooks bowser-help

## cost: tokens y costo equivalente de la rama actual (ALL=1: de todas las sesiones del proyecto)
cost:
	@python3 .bowser/costo.py $(if $(ALL),--todo,)

## verify: comprueba que la rama se puede cerrar (make check, pruebas, tamaño y revisión)
verify:
	@python3 .bowser/verificar.py

## hooks: activa los controles de git de este proyecto (una vez por clon)
hooks:
	@git config core.hooksPath .githooks && chmod +x .githooks/* && echo "✓ Controles de git activos (.githooks/)."

bowser-help:
	@grep -hE '^## ' $(MAKEFILE_LIST) | sed 's/^## /  make /'
