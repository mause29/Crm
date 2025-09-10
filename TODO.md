# Plan de Pruebas Exhaustivas Backend y Frontend

## Información Recopilada
- Backend: FastAPI con Socket.IO, dos archivos main (main.py simple, main_new.py completo)
- Frontend: React con Vite, API base localhost:8000, Socket.IO localhost:8000
- Servidores corriendo: Backend en 8000, Frontend en 5173
- Tests disponibles: test_critical_features.py, test_api.py, backend/test_integration.py
- start_server.py actualizado para usar main_new.py

## Plan Detallado
- [ ] Detener servidor backend actual (si usa main.py)
- [ ] Iniciar servidor backend con main_new.py
- [ ] Ejecutar pruebas de integración backend (test_integration.py)
- [ ] Ejecutar pruebas críticas del sistema (test_critical_features.py)
- [ ] Ejecutar pruebas de API (test_api.py)
- [ ] Verificar que frontend esté corriendo en localhost:5173
- [ ] Probar conexión frontend-backend usando browser
- [ ] Ejecutar pruebas de seguridad backend
- [ ] Corregir errores encontrados durante las pruebas

## Archivos Dependientes
- start_server.py (actualizado)
- backend/app/main_new.py (servidor completo)
- frontend/src/App.jsx (aplicación React)
- frontend/src/services/api.js (configuración API)
- frontend/src/socketClient.js (Socket.IO client)

## Pasos de Seguimiento
- Instalar dependencias faltantes si es necesario
- Verificar logs de servidor para errores
- Probar funcionalidades específicas (login, CRUD, notificaciones)
- Validar CORS y seguridad
- Documentar resultados de pruebas
