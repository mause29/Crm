# Guía de Implementación de Seguridad - CRM FastAPI

## 📋 Resumen Ejecutivo

Esta guía documenta la implementación completa de medidas de seguridad en el sistema CRM FastAPI, incluyendo autenticación JWT mejorada, middleware de seguridad, validación de entrada, gestión de sesiones y configuraciones de seguridad.

## 🔐 Características de Seguridad Implementadas

### 1. Autenticación y Autorización

#### JWT Mejorado
- **Tokens de Acceso**: 30 minutos de expiración
- **Tokens de Refresco**: 7 días de expiración
- **Claves Seguras**: Generadas automáticamente usando `secrets.token_urlsafe()`
- **Separación de Claves**: Claves diferentes para access y refresh tokens
- **Validación de Tipo**: Diferenciación entre access y refresh tokens

#### Gestión de Sesiones
- **Límite de Sesiones Concurrentes**: Máximo 5 sesiones por usuario
- **Timeout de Sesión**: 60 minutos de inactividad
- **Limpieza Automática**: Thread en background para sesiones expiradas
- **Información de Sesión**: IP, User-Agent, timestamps

### 2. Middleware de Seguridad

#### Rate Limiting
- **Límite por IP**: 60 requests por minuto
- **Exclusiones**: Rutas de documentación y health checks
- **Logging**: Eventos de rate limit excedido

#### Protección XSS
- **Detección de Patrones**: Scripts, iframes, event handlers
- **Sanitización**: Eliminación de contenido peligroso
- **Logging**: Alertas de intentos de XSS

#### Protección SQL Injection
- **Detección de Patrones**: Comentarios SQL, UNION SELECT, DROP TABLE
- **Validación**: Verificación de parámetros de query
- **Logging**: Alertas de intentos de SQL injection

#### Protección CSRF
- **Tokens CSRF**: Requeridos para métodos que modifican datos
- **Validación**: Verificación de tokens en headers
- **Exclusiones**: Rutas seguras como login y documentación

#### Headers de Seguridad
- **X-Content-Type-Options**: nosniff
- **X-Frame-Options**: DENY
- **X-XSS-Protection**: 1; mode=block
- **Strict-Transport-Security**: max-age=31536000
- **Content-Security-Policy**: default-src 'self'
- **Referrer-Policy**: strict-origin-when-cross-origin

### 3. Validación de Entrada

#### Sanitización de Datos
- **HTML Escaping**: Prevención de XSS básico
- **Sanitización HTML**: Limpieza de tags peligrosos
- **Validación de Email**: Dominios permitidos
- **Sanitización de Archivos**: Prevención de path traversal

#### Validación de Contraseñas
- **Longitud Mínima**: 8 caracteres
- **Requisitos**: Mayúsculas, minúsculas, dígitos, caracteres especiales
- **Validación en Tiempo Real**: Feedback inmediato

#### Validación de Archivos
- **Tamaño Máximo**: 5MB
- **Extensiones Permitidas**: jpg, png, pdf, doc, xls, txt
- **Verificación de Contenido**: Validación de tipo real

### 4. Configuración de Seguridad

#### Variables de Entorno
```bash
# JWT
SECRET_KEY=your-super-secret-key
REFRESH_SECRET_KEY=your-refresh-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Policy
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGITS=true
PASSWORD_REQUIRE_SPECIAL_CHARS=true

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Encryption
ENCRYPTION_KEY=your-encryption-key

# Session Management
SESSION_TIMEOUT_MINUTES=60
MAX_CONCURRENT_SESSIONS=5
```

#### Configuración CORS Mejorada
- **Orígenes Específicos**: Solo dominios permitidos
- **Métodos Específicos**: GET, POST, PUT, DELETE, OPTIONS, PATCH
- **Headers Específicos**: Authorization, Content-Type, X-CSRF-Token
- **Credenciales**: Habilitadas para cookies/autenticación
- **Cache**: 24 horas

### 5. Logging de Seguridad

#### Eventos Registrados
- **Acceso a API**: Todos los requests con metadata
- **Errores de API**: Status codes 4xx/5xx
- **Requests Lentos**: > 5 segundos
- **Intentos de XSS**: Patrones detectados
- **Intentos de SQL Injection**: Patrones detectados
- **Rate Limit Excedido**: IPs que exceden límites
- **Tokens CSRF Faltantes/Inválidos**: Validaciones fallidas

#### Formato de Log
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "event_type": "XSS_ATTEMPT_DETECTED",
  "user_id": 123,
  "ip_address": "192.168.1.100",
  "details": {
    "parameter": "search",
    "value": "<script>alert('xss')</script>",
    "pattern": "<script"
  }
}
```

### 6. Encriptación

#### Datos Sensibles
- **Encriptación Fernet**: Para datos sensibles en BD
- **Claves de Encriptación**: Gestionadas via variables de entorno
- **Rotación de Claves**: Soporte para rotación futura

## 🛠️ Uso de las Funcionalidades

### Autenticación JWT
```python
from app.auth import create_access_token, create_refresh_token, verify_token

# Crear tokens
access_token = create_access_token({"sub": "user@example.com"})
refresh_token = create_refresh_token({"sub": "user@example.com"})

# Verificar token
email = verify_token(access_token)
```

### Gestión de Sesiones
```python
from app.utils.session_manager import session_manager

# Crear sesión
session_id = session_manager.create_session(
    user_id=123,
    email="user@example.com",
    ip_address="192.168.1.100",
    user_agent="Mozilla/5.0..."
)

# Validar sesión
is_valid = session_manager.validate_session(session_id, 123)

# Invalidar sesiones
session_manager.invalidate_user_sessions(123)
```

### Validación de Entrada
```python
from app.utils.security import sanitize_input, validate_password_strength

# Sanitizar datos
clean_data = sanitize_input(request_data)

# Validar contraseña
result = validate_password_strength("MySecurePass123!")
# {"length": true, "uppercase": true, "lowercase": true, "digit": true, "special_char": false, "overall": false}
```

### Middleware de Seguridad
```python
from app.middleware.security import add_security_middleware

# Añadir middleware a la app
add_security_middleware(app, {
    "enable_rate_limiting": True,
    "enable_xss_protection": True,
    "enable_csrf_protection": True,
    "rate_limit_requests": 60
})
```

## 🔍 Monitoreo y Alertas

### Métricas de Seguridad
- **Intentos de Login Fallidos**: Por usuario/IP
- **Sesiones Activas**: Por usuario
- **Rate Limits Excedidos**: Por endpoint/IP
- **Ataques Detectados**: XSS, SQLi, CSRF

### Alertas Recomendadas
- **Múltiples Fallos de Login**: Posible ataque de fuerza bruta
- **Sesiones Concurrentes Altas**: Posible robo de credenciales
- **Ataques Detectados**: Revisión inmediata requerida
- **Rate Limits Excedidos**: Posible ataque DoS

## 🚀 Mejores Prácticas Implementadas

### 1. Principio de Menor Privilegio
- Tokens con expiración corta
- Sesiones limitadas por usuario
- Headers de seguridad restrictivos

### 2. Defensa en Profundidad
- Múltiples capas de validación
- Sanitización en múltiples puntos
- Logging comprehensivo

### 3. Fail-Safe Defaults
- Configuraciones seguras por defecto
- Validación estricta de entrada
- Manejo robusto de errores

### 4. Zero Trust
- Verificación en cada request
- No confiar en inputs del usuario
- Validación de todas las entradas

## 📊 Testing de Seguridad

### Pruebas Automatizadas
```bash
# Ejecutar pruebas de seguridad
python -m pytest tests/test_security.py -v

# Ejecutar pruebas de integración
python test_integration.py
```

### Pruebas Manuales Recomendadas
1. **SQL Injection**: Intentar payloads comunes en parámetros
2. **XSS**: Probar scripts en campos de entrada
3. **CSRF**: Intentar requests sin tokens CSRF
4. **Rate Limiting**: Exceder límites de requests
5. **Session Hijacking**: Intentar usar tokens expirados

## 🔧 Mantenimiento

### Rotación de Claves
```bash
# Generar nuevas claves
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Actualizar variables de entorno
export SECRET_KEY=new_secret_key
export REFRESH_SECRET_KEY=new_refresh_key
```

### Monitoreo de Logs
```bash
# Buscar eventos de seguridad
grep "SECURITY_EVENT" /var/log/crm/security.log

# Contar ataques detectados
grep "ATTEMPT_DETECTED" /var/log/crm/security.log | wc -l
```

### Actualizaciones de Seguridad
- **Mantener Dependencias Actualizadas**: Regularmente actualizar FastAPI, Jose, etc.
- **Revisar Configuraciones**: Periódicamente auditar configuraciones de seguridad
- **Monitorear Logs**: Configurar alertas para eventos de seguridad críticos

## 📈 Próximas Mejoras

### Funcionalidades Planificadas
1. **2FA (Two-Factor Authentication)**
2. **OAuth2 Integration**
3. **API Key Management**
4. **Advanced Threat Detection**
5. **Security Dashboard**

### Mejoras de Rendimiento
1. **Redis para Rate Limiting**
2. **Database Indexing para Logs**
3. **Asynchronous Security Processing**
4. **Caching de Configuraciones**

---

## 📞 Contacto y Soporte

Para preguntas sobre la implementación de seguridad o reportes de vulnerabilidades, contactar al equipo de desarrollo.

**Última Actualización**: Enero 2024
**Versión**: 1.0.0
