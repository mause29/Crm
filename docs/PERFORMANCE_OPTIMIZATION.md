# 🚀 Optimizaciones de Rendimiento

Este documento describe las optimizaciones de rendimiento implementadas en el sistema CRM, incluyendo paginación, caché y monitoreo de rendimiento.

## 📋 Características Implementadas

### 1. Paginación Inteligente

**Archivo:** `backend/app/routes/users_paginated.py`

#### Características:
- **Paginación eficiente** para grandes volúmenes de datos
- **Parámetros configurables:**
  - `page`: Número de página (por defecto: 1)
  - `per_page`: Elementos por página (1-100, por defecto: 10)
  - `active_only`: Solo usuarios activos (por defecto: true)
  - `role`: Filtrar por rol específico

#### Ejemplo de uso:
```bash
GET /users/?page=2&per_page=20&active_only=true&role=admin
```

#### Respuesta paginada:
```json
{
  "items": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": true
  }
}
```

### 2. Sistema de Caché Avanzado

**Archivo:** `backend/app/utils/cache.py`

#### Características:
- **Caché en memoria** con Redis como backend opcional
- **TTL configurable** por tipo de dato
- **Invalidación inteligente** de caché
- **Compresión automática** para respuestas grandes

#### Configuración de caché:
```python
# En settings.py
CACHE_TTL_USERS = 300  # 5 minutos
CACHE_TTL_CLIENTS = 600  # 10 minutos
CACHE_TTL_REPORTS = 1800  # 30 minutos
```

#### Funciones principales:
- `get_cached_user_list()`: Obtiene lista de usuarios del caché
- `set_cached_user_list()`: Almacena lista de usuarios en caché
- `invalidate_user_cache()`: Invalida caché de usuarios

### 3. Monitoreo de Rendimiento

**Archivo:** `backend/app/utils/performance.py`

#### Características:
- **Monitoreo en tiempo real** de endpoints
- **Métricas de sistema** (CPU, memoria, disco)
- **Estadísticas de rendimiento** por endpoint
- **Percentiles P95/P99** para análisis de latencia

#### Endpoints de monitoreo:
```bash
GET /performance/stats  # Estadísticas detalladas
GET /health            # Verificación de salud
```

#### Métricas disponibles:
- **Tiempo de respuesta promedio**
- **Percentiles P95 y P99**
- **Número total de requests**
- **Uso de recursos del sistema**

### 4. Optimización de Consultas

**Características:**
- **Consultas optimizadas** con índices apropiados
- **Timeout de consultas** para prevenir bloqueos
- **Pool de conexiones** configurado para alto rendimiento
- **Compresión de respuestas** automática

#### Configuración de base de datos:
```python
db_config = {
    "pool_pre_ping": True,      # Verificar conexiones
    "pool_recycle": 3600,       # Reciclar cada hora
    "pool_size": 10,            # Tamaño del pool
    "max_overflow": 20,         # Overflow máximo
    "pool_timeout": 30,         # Timeout del pool
}
```

## 🛠️ Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r backend/requirements-performance.txt
```

### 2. Configurar Redis (opcional)
```bash
# Instalar Redis
sudo apt-get install redis-server

# Iniciar Redis
redis-server

# Configurar en settings.py
REDIS_URL = "redis://localhost:6379"
USE_REDIS_CACHE = True
```

### 3. Configurar variables de entorno
```bash
# En .env
CACHE_TTL_USERS=300
CACHE_TTL_CLIENTS=600
DEFAULT_PAGE_SIZE=10
MAX_PAGE_SIZE=100
```

## 📊 Uso y Monitoreo

### Verificar rendimiento
```bash
# Estadísticas de rendimiento
curl http://localhost:8000/performance/stats

# Verificación de salud
curl http://localhost:8000/health
```

### Monitoreo en producción
```python
from backend.app.utils.performance import performance_monitor

# Obtener métricas
stats = await get_performance_stats()
print(f"CPU Usage: {stats['system']['cpu_percent']}%")
print(f"Memory Usage: {stats['system']['memory_percent']}%")
```

## 🔧 Optimizaciones Adicionales

### 1. Compresión de Respuestas
```python
from backend.app.utils.performance import CompressedJSONResponse

@app.get("/large-data")
async def get_large_data():
    data = await fetch_large_dataset()
    return CompressedJSONResponse(content=data)
```

### 2. Procesamiento Asíncrono por Lotes
```python
from backend.app.utils.performance import async_batch_processor

# Procesar datos en lotes
results = await async_batch_processor(
    items=large_dataset,
    processor=process_item,
    batch_size=10
)
```

### 3. Optimización de Memoria
```python
from backend.app.utils.performance import memory_efficient_iterator

# Iterar eficientemente sobre datos grandes
for batch in memory_efficient_iterator(large_list, chunk_size=100):
    await process_batch(batch)
```

## 📈 Mejoras de Rendimiento Esperadas

### Antes de la optimización:
- **Tiempo de respuesta:** ~500-1000ms para listas grandes
- **Uso de memoria:** Alto para datasets grandes
- **Escalabilidad:** Limitada por consultas N+1

### Después de la optimización:
- **Tiempo de respuesta:** ~50-200ms con caché
- **Uso de memoria:** Optimizado con paginación
- **Escalabilidad:** Mejorada con pool de conexiones
- **Disponibilidad:** Monitoreo proactivo

## 🚨 Alertas y Monitoreo

### Métricas críticas a monitorear:
- **Tiempo de respuesta > 500ms**
- **Uso de CPU > 80%**
- **Uso de memoria > 85%**
- **Errores de caché > 5%**

### Configuración de alertas:
```python
# En settings.py
ALERT_RESPONSE_TIME_THRESHOLD = 500  # ms
ALERT_CPU_THRESHOLD = 80  # %
ALERT_MEMORY_THRESHOLD = 85  # %
ALERT_CACHE_ERROR_THRESHOLD = 5  # %
```

## 🔍 Troubleshooting

### Problemas comunes:

1. **Caché no funciona:**
   - Verificar configuración de Redis
   - Comprobar conectividad a Redis
   - Revisar logs de errores

2. **Consultas lentas:**
   - Verificar índices de base de datos
   - Comprobar configuración del pool
   - Analizar queries con EXPLAIN

3. **Alto uso de memoria:**
   - Implementar paginación
   - Usar iteradores eficientes
   - Configurar límites de memoria

4. **Timeouts de conexión:**
   - Ajustar configuración del pool
   - Implementar retry logic
   - Configurar timeouts apropiados

## 📚 Referencias

- [FastAPI Performance Tips](https://fastapi.tiangolo.com/tutorial/performance/)
- [SQLAlchemy Optimization](https://docs.sqlalchemy.org/en/14/faq/performance.html)
- [Redis Caching Patterns](https://redis.io/documentation)
- [Python AsyncIO Best Practices](https://docs.python.org/3/library/asyncio.html)

## 🤝 Contribución

Para contribuir con optimizaciones adicionales:

1. **Medir antes y después** de cualquier cambio
2. **Documentar mejoras** en este archivo
3. **Agregar tests** para nuevas funcionalidades
4. **Actualizar métricas** de monitoreo

---

*Última actualización: Diciembre 2024*
