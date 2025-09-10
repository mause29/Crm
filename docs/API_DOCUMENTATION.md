# Documentación de la API CRM Completo

## Introducción

Esta documentación cubre los endpoints disponibles en la API del sistema CRM Completo con PayPal y ML. La API está construida con FastAPI y documentada con OpenAPI 3.0, accesible en `/docs` y `/redoc`.

## Autenticación

- La mayoría de los endpoints requieren autenticación JWT.
- El token debe enviarse en el header `Authorization` como:  
  `Bearer <token>`

## Endpoints Principales

### Usuarios

- **POST /users/**  
  Crear un nuevo usuario.  
  Requiere: nombre, email, contraseña, rol (opcional), company_id (opcional).  
  Respuesta: ID del usuario creado.

- **POST /users/token**  
  Login con email y contraseña.  
  Respuesta: token JWT.

- **POST /users/token/2fa**  
  Login con 2FA.

- **POST /users/enable-2fa/{user_id}**  
  Habilitar 2FA para un usuario.

- **GET /users/**  
  Obtener lista de usuarios (admin).

- **GET /users/{user_id}**  
  Obtener detalles de un usuario.

### Clientes

- **GET /clients/**  
  Obtener lista de clientes de la compañía.

- **POST /clients/**  
  Crear un nuevo cliente.

### Oportunidades, Facturas, Gamificación, Notificaciones, Reportes, Tareas, Analytics, Dashboard, Email, Filtering

- Endpoints para gestión avanzada, consultar documentación específica en `/docs`.

## Ejemplos de Uso

Para cada endpoint, consultar la documentación interactiva en `/docs` para ejemplos detallados de request y response.

## Contacto

Para soporte, contactar a: support@crm.com

## Licencia

MIT License
