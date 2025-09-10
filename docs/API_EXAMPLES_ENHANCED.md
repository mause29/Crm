# 📋 Ejemplos de Uso de la API CRM

## 🚀 Guía Completa de Ejemplos

Esta guía proporciona ejemplos prácticos de cómo usar la API del sistema CRM. Todos los ejemplos incluyen las llamadas HTTP completas, headers necesarios y respuestas esperadas.

---

## 🔐 Autenticación

### 1. Crear Usuario

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan.perez@empresa.com",
    "password": "SecurePass123",
    "role": "user"
  }'
```

**Respuesta exitosa:**
```json
{
  "msg": "User created successfully",
  "user_id": 1
}
```

### 2. Iniciar Sesión

```bash
curl -X POST "http://localhost:8000/users/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan.perez@empresa.com&password=SecurePass123"
```

**Respuesta exitosa:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 👥 Gestión de Clientes

### 1. Crear Cliente

```bash
curl -X POST "http://localhost:8000/clients/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "name=María García&email=maria.garcia@cliente.com&phone=+34612345678"
```

**Respuesta exitosa:**
```json
{
  "msg": "Client created",
  "client_id": 1
}
```

### 2. Obtener Lista de Clientes

```bash
curl -X GET "http://localhost:8000/clients/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Respuesta exitosa:**
```json
[
  {
    "id": 1,
    "name": "María García",
    "email": "maria.garcia@cliente.com",
    "phone": "+34 612 345 678",
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Carlos Rodríguez",
    "email": "carlos.rodriguez@empresa.com",
    "phone": "+34 698 765 432",
    "created_at": "2024-01-10T14:20:00Z"
  }
]
```

---

## 💼 Gestión de Oportunidades

### 1. Crear Oportunidad

```bash
curl -X POST "http://localhost:8000/opportunities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Proyecto Desarrollo Web",
    "value": 15000.50,
    "client_id": 1
  }'
```

**Respuesta exitosa:**
```json
{
  "msg": "Opportunity created"
}
```

### 2. Obtener Lista de Oportunidades

```bash
curl -X GET "http://localhost:8000/opportunities/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Respuesta exitosa:**
```json
[
  {
    "id": 1,
    "name": "Proyecto Desarrollo Web",
    "value": 15000.50,
    "client_id": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "status": "active"
  }
]
```

---

## 💰 Gestión de Facturas

### 1. Crear Factura

```bash
curl -X POST "http://localhost:8000/invoices/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "client_id": 1,
    "amount": 2500.75
  }'
```

**Respuesta exitosa:**
```json
{
  "msg": "Invoice created"
}
```

### 2. Procesar Pago de Factura

```bash
curl -X POST "http://localhost:8000/invoices/pay/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Respuesta exitosa:**
```json
{
  "msg": "Invoice paid"
}
```

---

## 📊 Monitoreo y Salud del Sistema

### 1. Verificación de Salud

```bash
curl -X GET "http://localhost:8000/health"
```

**Respuesta exitosa:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "version": "1.0.0",
  "performance": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "disk_usage": 234567890
  }
}
```

### 2. Estadísticas de Rendimiento

```bash
curl -X GET "http://localhost:8000/performance/stats" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Respuesta exitosa:**
```json
{
  "system": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "disk_usage": 234567890
  },
  "endpoints": {
    "/users/": {
      "avg_response_time": 0.234,
      "total_requests": 1250,
      "error_rate": 0.02
    }
  }
}
```

---

## 🛠️ Ejemplos con JavaScript (Node.js)

### Configuración Inicial

```javascript
const axios = require('axios');

const API_BASE_URL = 'http://localhost:8000';
let authToken = null;

// Función para iniciar sesión
async function login(email, password) {
  try {
    const response = await axios.post(`${API_BASE_URL}/users/token`, {
      username: email,
      password: password
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    authToken = response.data.access_token;
    console.log('✅ Login exitoso');
    return authToken;
  } catch (error) {
    console.error('❌ Error en login:', error.response.data);
    throw error;
  }
}

// Función para hacer requests autenticados
async function apiRequest(method, endpoint, data = null) {
  try {
    const config = {
      method: method,
      url: `${API_BASE_URL}${endpoint}`,
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    };

    if (data) {
      if (method === 'post' && typeof data === 'object') {
        config.data = data;
        config.headers['Content-Type'] = 'application/json';
      }
    }

    const response = await axios(config);
    return response.data;
  } catch (error) {
    console.error(`❌ Error en ${method.toUpperCase()} ${endpoint}:`, error.response.data);
    throw error;
  }
}
```

### Ejemplo Completo de Uso

```javascript
async function ejemploCompleto() {
  try {
    // 1. Iniciar sesión
    await login('juan.perez@empresa.com', 'SecurePass123');

    // 2. Crear un cliente
    const cliente = await apiRequest('post', '/clients/', {
      name: 'María García',
      email: 'maria.garcia@cliente.com',
      phone: '+34612345678'
    });
    console.log('Cliente creado:', cliente);

    // 3. Crear una oportunidad
    const oportunidad = await apiRequest('post', '/opportunities/', {
      name: 'Proyecto Desarrollo Web',
      value: 15000.50,
      client_id: cliente.client_id
    });
    console.log('Oportunidad creada:', oportunidad);

    // 4. Crear una factura
    const factura = await apiRequest('post', '/invoices/', {
      client_id: cliente.client_id,
      amount: 2500.75
    });
    console.log('Factura creada:', factura);

    // 5. Obtener lista de clientes
    const clientes = await apiRequest('get', '/clients/');
    console.log('Lista de clientes:', clientes);

    // 6. Verificar salud del sistema
    const health = await axios.get(`${API_BASE_URL}/health`);
    console.log('Estado del sistema:', health.data);

  } catch (error) {
    console.error('Error en el ejemplo:', error.message);
  }
}

// Ejecutar ejemplo
ejemploCompleto();
```

---

## 🐍 Ejemplos con Python

### Configuración Inicial

```python
import requests
import json

API_BASE_URL = 'http://localhost:8000'
auth_token = None

def login(email: str, password: str) -> str:
    """Inicia sesión y retorna el token JWT"""
    response = requests.post(
        f"{API_BASE_URL}/users/token",
        data={
            "username": email,
            "password": password
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if response.status_code == 200:
        global auth_token
        auth_token = response.json()["access_token"]
        print("✅ Login exitoso")
        return auth_token
    else:
        print(f"❌ Error en login: {response.json()}")
        raise Exception("Login failed")

def api_request(method: str, endpoint: str, data=None) -> dict:
    """Hace una request autenticada a la API"""
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    if data and method.lower() == "post":
        headers["Content-Type"] = "application/json"
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=data,
            headers=headers
        )
    else:
        response = requests.request(
            method.upper(),
            f"{API_BASE_URL}{endpoint}",
            headers=headers
        )

    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"❌ Error en {method.upper()} {endpoint}: {response.json()}")
        raise Exception(f"API request failed: {response.status_code}")
```

### Ejemplo Completo de Uso

```python
def ejemplo_completo():
    try:
        # 1. Iniciar sesión
        login('juan.perez@empresa.com', 'SecurePass123')

        # 2. Crear un cliente
        cliente = api_request('post', '/clients/', {
            "name": "María García",
            "email": "maria.garcia@cliente.com",
            "phone": "+34612345678"
        })
        print(f"Cliente creado: {cliente}")

        # 3. Crear una oportunidad
        oportunidad = api_request('post', '/opportunities/', {
            "name": "Proyecto Desarrollo Web",
            "value": 15000.50,
            "client_id": cliente["client_id"]
        })
        print(f"Oportunidad creada: {oportunidad}")

        # 4. Crear una factura
        factura = api_request('post', '/invoices/', {
            "client_id": cliente["client_id"],
            "amount": 2500.75
        })
        print(f"Factura creada: {factura}")

        # 5. Obtener lista de clientes
        clientes = api_request('get', '/clients/')
        print(f"Lista de clientes: {json.dumps(clientes, indent=2)}")

        # 6. Verificar salud del sistema
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print(f"Estado del sistema: {json.dumps(response.json(), indent=2)}")

    except Exception as error:
        print(f"Error en el ejemplo: {error}")

# Ejecutar ejemplo
if __name__ == "__main__":
    ejemplo_completo()
```

---

## 📱 Ejemplos con Postman

### 1. Configuración de Variables

En Postman, crea un nuevo environment con estas variables:
- `base_url`: `http://localhost:8000`
- `token`: (se actualizará automáticamente)

### 2. Collection de Ejemplos

```json
{
  "info": {
    "name": "CRM API Examples",
    "description": "Ejemplos completos de uso de la API CRM"
  },
  "item": [
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/x-www-form-urlencoded"
          }
        ],
        "body": {
          "mode": "urlencoded",
          "urlencoded": [
            {
              "key": "username",
              "value": "juan.perez@empresa.com"
            },
            {
              "key": "password",
              "value": "SecurePass123"
            }
          ]
        },
        "url": {
          "raw": "{{base_url}}/users/token",
          "host": ["{{base_url}}"],
          "path": ["users", "token"]
        },
        "event": [
          {
            "listen": "test",
            "script": {
              "exec": [
                "if (pm.response.code === 200) {",
                "    const response = pm.response.json();",
                "    pm.environment.set('token', response.access_token);",
                "}"
              ]
            }
          }
        ]
      }
    },
    {
      "name": "Create Client",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          },
          {
            "key": "Content-Type",
            "value": "application/x-www-form-urlencoded"
          }
        ],
        "body": {
          "mode": "urlencoded",
          "urlencoded": [
            {
              "key": "name",
              "value": "María García"
            },
            {
              "key": "email",
              "value": "maria.garcia@cliente.com"
            },
            {
              "key": "phone",
              "value": "+34612345678"
            }
          ]
        },
        "url": {
          "raw": "{{base_url}}/clients/",
          "host": ["{{base_url}}"],
          "path": ["clients", ""]
        }
      }
    }
  ]
}
```

---

## ⚠️ Manejo de Errores

### Errores Comunes y Soluciones

#### 1. Error 401 - No autorizado
```json
{
  "detail": "Not authenticated"
}
```
**Solución:** Verificar que el token JWT sea válido y esté incluido en el header `Authorization: Bearer <token>`

#### 2. Error 400 - Datos inválidos
```json
{
  "detail": "Client with this email already exists"
}
```
**Solución:** Verificar que los datos enviados cumplan con las validaciones requeridas

#### 3. Error 404 - Recurso no encontrado
```json
{
  "detail": "Invoice not found"
}
```
**Solución:** Verificar que el ID del recurso exista en la base de datos

#### 4. Error 500 - Error interno del servidor
```json
{
  "detail": "Internal server error"
}
```
**Solución:** Revisar los logs del servidor para más detalles sobre el error

---

## 🔧 Tips para Desarrollo

### 1. Rate Limiting
La API incluye protección contra abuso con límites de tasa. Si excedes los límites, recibirás un error 429.

### 2. Compresión de Respuestas
Las respuestas grandes se comprimen automáticamente para mejorar el rendimiento.

### 3. Caché
Algunos endpoints utilizan caché inteligente para mejorar la velocidad de respuesta.

### 4. Logging
Todas las operaciones importantes se registran para auditoría y debugging.

---

## 📞 Soporte

Si encuentras problemas o necesitas ayuda adicional:

- 📧 **Email**: support@crm.com
- 📚 **Documentación**: `/docs` (Swagger UI)
- 🔄 **Estado**: `/health` (verificación de salud)
- 📊 **Rendimiento**: `/performance/stats` (estadísticas del sistema)
