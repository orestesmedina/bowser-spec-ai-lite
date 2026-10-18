# Principios del kit

<!-- Archivo de bowser-ai-lite: se reemplaza al actualizar el kit y vale para cualquier proyecto y tecnología.
     Lo propio de cada proyecto va en AGENTS.md, que puede agregar o endurecer reglas, nunca quitar estas. -->

Estas reglas no se negocian dentro de una tarea. Si cumplirlas exige algo que la tarea no cubre, detente y avisa.

## Seguridad
1. Consultas a la base de datos siempre con parámetros; nunca armar SQL concatenando texto. (CWE-89)
2. Validar toda entrada en el servidor, aunque el cliente ya valide. (CWE-20)
3. Escapar todo dato que se muestra, según dónde se muestra (HTML, atributo, URL, JavaScript). (CWE-79)
4. Contraseñas con un algoritmo hecho para contraseñas (bcrypt o argon2). Nunca en texto plano ni con un hash rápido. (CWE-256)
5. Secretos y configuración desde variables de entorno. Nunca en el código, en git, en los mensajes ni en los registros. (CWE-798)
6. Autenticación y autorización verificadas en el servidor en cada acceso protegido. (CWE-862)
7. Ninguna dependencia nueva con vulnerabilidades altas o críticas conocidas.
8. Datos personales: solo los necesarios, y nunca en registros, mensajes de error ni datos de prueba reales.

## Calidad
9. Todo cambio de comportamiento lleva su prueba, salvo que `AGENTS.md` diga otro alcance para esa parte.
10. Nada se entrega con pruebas fallando. Una prueba no se debilita ni se desactiva para que pase, y los controles (`.bowser/verificacion`, hooks, CI) no se aflojan para que algo pase.
11. El código pasa el formato y la revisión del proyecto (`make check`).

## Datos
12. Todo cambio de esquema va en un archivo versionado nuevo, con la forma de revertirlo. Un cambio ya aplicado no se modifica.
13. Nada que borre o reescriba datos en masa sin que una persona lo pida.

## Personas
14. Subir cambios, hacer merge a la rama principal y desplegar lo decide una persona.
15. Si el pedido es ambiguo en algo que cambia el resultado (una regla de negocio, un permiso, un dato), se pregunta. No se inventa.
16. Lo que se encuentra fuera de la tarea (deuda, riesgos) se anota en `docs/memoria/deuda.md`; no se arregla de paso.
