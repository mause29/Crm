# Ejemplos de Uso de la API CRM

## 1. Crear Usuario

```bash
curl -X POST "http://localhost:8000/users/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Juan Pérez",
  "email": "juan.perez@empresa.com",
  "password": "SecurePass123",
  "role": "user",
  "company_id": 1
}'
```

Respuesta:
```json
{
  "msg": "User created successfully",
  "user_id": 1
}
```

## 2. Login

```bash
curl -X POST "http://localhost:8000/users/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=juan.perez@empresa.com&password=SecurePass123"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 3. Crear Cliente (Requiere Token)

```bash
curl -X POST "http://localhost:8000/clients/" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
-d "name=María García&email=maria.garcia@cliente.com&phone=+34612345678"
```

Respuesta:
```json
{
  "msg": "Client created",
  "client_id": 1
}
```

## 4. Obtener Clientes

```bash
curl -X GET "http://localhost:8000/clients/" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Respuesta:
```json
[
  {
    "id": 1,
    "name": "María García",
    "email": "maria.garcia@cliente.com",
    "phone": "+34612345678",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

## 5. Crear Oportunidad

```bash
curl -X POST "http://localhost:8000/opportunities/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
-d '{
  "name": "Proyecto Desarrollo Web",
  "value": 15000.50,
  "client_id": 1
}'
```

## 6. Crear Factura

```bash
curl -X POST "http://localhost:8000/invoices/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
-d '{
  "client_id": 1,
  "amount": 2500.75,
  "due_date": "2024-12-31"
}'
```

## 7. Obtener Notificaciones

```bash
curl -X GET "http://localhost:8000/notifications/" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 8. Obtener Dashboard

```bash
curl -X GET "http://localhost:8000/dashboard/" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 9. Obtener Reportes

```bash
curl -X GET "http://localhost:8000/reports/" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 10. Obtener Analytics

```bash
curl -X GET "http://localhost:8000/analytics/" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Notas Importantes

- Todos los endpoints requieren autenticación JWT excepto `/users/` (crear usuario)
- Los tokens expiran en 30 minutos por defecto
- Las fechas deben estar en formato YYYY-MM-DD
- Los teléfonos deben incluir código de país (+XX)
- Los emails deben ser únicos en el sistema
