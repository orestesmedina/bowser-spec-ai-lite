# Requerimientos

<!-- Qué debe hacer el sistema y para quién. Formato en .bowser/documentacion.md.
     Proyecto nuevo: se escribe desde la idea, antes del código. Proyecto existente: se escribe leyendo el
     código y la base de datos, con estado "existe" y dónde se vio. Las funcionalidades nuevas lo actualizan. -->

Origen: <idea | descubierto del código el AAAA-MM-DD>. Última revisión: <AAAA-MM-DD>.

## Visión
- **Problema:** <qué duele hoy y a quién.>
- **Para quién:** <tipos de usuario.>
- **Cómo sabremos que funciona:** <1 a 3 resultados medibles: "un pedido se registra en menos de 2 minutos".>

## Usuarios y roles
| Rol | Quién es | Qué puede hacer |
|---|---|---|
| <Cliente> | <Persona que compra en la tienda> | <Ver catálogo, comprar, ver sus pedidos> |
| <Administrador> | <Personal de la empresa> | <Gestionar productos y pedidos> |

## Alcance
- **Sí incluye:** <lo que entra en esta versión.>
- **No incluye:** <lo que se deja fuera a propósito, para que nadie lo construya "de paso".>

## Requisitos funcionales

### RF-01 · <Registro de clientes>
- **Quién y para qué:** <un visitante crea su cuenta para poder comprar.>
- **Estado:** <planeado | en curso | existe | descartado>. **Roadmap:** <#2>. **Dónde se vio:** <solo si es descubierto: `backend/internal/usuarios/handler.go:42`>
- **Criterios de aceptación:**
  - Dado <un correo que no está registrado>, cuando <envía el formulario con datos válidos>, entonces <se crea la cuenta y recibe un correo de confirmación>.
  - Dado <un correo ya registrado>, cuando <intenta registrarse>, entonces <ve un aviso y no se crea otra cuenta>.

## Requisitos no funcionales
| Id | Tipo | Requisito comprobable |
|---|---|---|
| <RNF-01> | <Rendimiento> | <El catálogo carga en menos de 1 s con 500 productos> |
| <RNF-02> | <Disponibilidad> | <Se puede desplegar sin cortar el servicio más de 1 minuto> |

## Restricciones
<!-- Lo que viene impuesto: tecnología obligada, hosting, presupuesto, leyes, integraciones existentes. -->
- <Debe correr en el servidor actual del cliente (Ubuntu 24.04, 4 GB de RAM).>

## Preguntas abiertas
<!-- Lo que falta decidir. Cada una con una recomendación. Al responderse, pasa a un requisito o a decisiones.md. -->
- <¿Los administradores pueden borrar pedidos o solo cancelarlos? Recomendación: solo cancelar, por auditoría.>

## Glosario
<!-- Términos del negocio con un significado preciso en este proyecto. -->
| Término | Significa |
|---|---|
| <Pedido> | <Una compra confirmada y pagada; antes de pagar es "carrito"> |
