"""
Utilidades de optimización de rendimiento para la API.
Incluye compresión de respuestas, optimización de consultas y monitoreo.
"""
import time
import gzip
import json
import logging
from typing import Any, Dict, List, Optional, Callable, Union
from functools import wraps
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import psutil
import os
from ..config.settings import settings

# Configurar logging para performance
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """
    Monitor de rendimiento para endpoints y operaciones críticas.
    """

    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)

    def record_metric(self, name: str, duration: float):
        """Registra una métrica de rendimiento."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(duration)

        # Mantener solo las últimas 1000 mediciones
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]

    def get_average(self, name: str) -> Optional[float]:
        """Obtiene el promedio de una métrica."""
        if name in self.metrics and self.metrics[name]:
            return sum(self.metrics[name]) / len(self.metrics[name])
        return None

    def get_percentile(self, name: str, percentile: float) -> Optional[float]:
        """Obtiene el percentil de una métrica."""
        if name in self.metrics and self.metrics[name]:
            sorted_metrics = sorted(self.metrics[name])
            index = int(len(sorted_metrics) * percentile / 100)
            return sorted_metrics[min(index, len(sorted_metrics) - 1)]
        return None

    def get_system_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema con optimización de CPU."""
        # Cache system stats to reduce CPU usage
        current_time = time.time()
        if not hasattr(self, '_last_system_stats_time') or current_time - self._last_system_stats_time > 5:
        
                "cpu_percent": psutil.cpu_percent(interval=0.5),  # Reduced interval
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_connections": len(psutil.net_connections()),
            }
            self._last_system_stats_time = current_time

        return self._cached_system_stats
# Instancia global del monitor
performance_monitor = PerformanceMonitor()

def performance_monitoring(operation_name: str):
    """
    Decorador para monitorear el rendimiento de funciones.

    Args:
        operation_name: Nombre de la operación a monitorear
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                performance_monitor.record_metric(operation_name, duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                performance_monitor.record_metric(f"{operation_name}_error", duration)
                raise e

        return wrapper
    return decorator

class CompressedJSONResponse(JSONResponse):
    """
    Respuesta JSON comprimida para reducir el tamaño de la respuesta.
    """

    def __init__(self, content: Any, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        super().__init__(content, status_code, headers)

    async def __call__(self, scope, receive, send):
        # Comprimir solo si el contenido es lo suficientemente grande
        if len(self.body) > 1024:  # Comprimir si > 1KB
            compressed_body = await asyncio.get_event_loop().run_in_executor(
                performance_monitor.executor,
                gzip.compress,
                self.body
            )
            self.body = compressed_body
            self.headers["Content-Encoding"] = "gzip"
            self.headers["Content-Length"] = str(len(compressed_body))

        await super().__call__(scope, receive, send)

def create_compressed_response(data: Any, status_code: int = 200) -> CompressedJSONResponse:
    """
    Crea una respuesta JSON comprimida.

    Args:
        data: Datos a serializar
        status_code: Código de estado HTTP

    Returns:
        CompressedJSONResponse: Respuesta comprimida
    """
    return CompressedJSONResponse(content=data, status_code=status_code)

class QueryOptimizer:
    """
    Optimizador de consultas de base de datos.
    """

    @staticmethod
    def optimize_user_query(query, filters: Dict[str, Any] = None):
        """
        Optimiza consultas de usuarios con índices apropiados.

        Args:
            query: Query base de SQLAlchemy
            filters: Filtros adicionales

        Returns:
            Query optimizada
        """
        # Aplicar filtros de manera eficiente
        if filters:
            if 'active_only' in filters and filters['active_only']:
                query = query.filter_by(is_active=True)

            if 'role' in filters:
                query = query.filter_by(role=filters['role'])

            if 'company_id' in filters:
                query = query.filter_by(company_id=filters['company_id'])

            if 'created_after' in filters:
                query = query.filter(query.model.created_at >= filters['created_after'])

            if 'created_before' in filters:
                query = query.filter(query.model.created_at <= filters['created_before'])

        return query

    @staticmethod
    def add_pagination(query, page: int, per_page: int):
        """
        Agrega paginación eficiente a una consulta.

        Args:
            query: Query de SQLAlchemy
            page: Número de página
            per_page: Elementos por página

        Returns:
            Query paginada
        """
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page)

    @staticmethod
    async def execute_with_timeout(query, timeout_seconds: int = 30):
        """
        Ejecuta una consulta con timeout para prevenir consultas lentas.

        Args:
            query: Query de SQLAlchemy
            timeout_seconds: Timeout en segundos

        Returns:
            Resultados de la consulta
        """
        try:
            # Ejecutar en un executor para poder aplicar timeout
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    performance_monitor.executor,
                    lambda: query.all()
                ),
                timeout=timeout_seconds
            )
            return result
        except asyncio.TimeoutError:
            raise Exception(f"Query timeout after {timeout_seconds} seconds")

class ResponseOptimizer:
    """
    Optimizador de respuestas para mejorar el rendimiento del cliente.
    """

    @staticmethod
    def minimize_user_response(users: List[Any]) -> List[Dict[str, Any]]:
        """
        Minimiza la respuesta de usuarios eliminando campos innecesarios.

        Args:
            users: Lista de objetos User

        Returns:
            Lista de diccionarios minimizados
        """
        minimized = []
        for user in users:
            minimized.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            })
        return minimized

    @staticmethod
    def create_etag(data: Any) -> str:
        """
        Crea un ETag para la respuesta basado en el contenido.

        Args:
            data: Datos para generar el ETag

        Returns:
            ETag string
        """
        import hashlib
        content = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(content.encode()).hexdigest()

def cached_endpoint(ttl_seconds: int = 300):
    """
    Decorador para endpoints con caché inteligente.

    Args:
        ttl_seconds: Tiempo de vida del caché en segundos
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extraer request de los argumentos
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if request:
                # Crear clave de caché basada en la URL y parámetros
                cache_key = f"{request.url.path}?{request.url.query}"

                # Verificar si hay un ETag en los headers
                if_etag = request.headers.get("If-None-Match")
                if if_etag:
                    # Aquí podrías verificar contra el caché
                    pass

                # Medir tiempo de respuesta
                start_time = time.time()

                result = await func(*args, **kwargs)

                duration = time.time() - start_time
                performance_monitor.record_metric(func.__name__, duration)

                # Agregar headers de rendimiento
                if isinstance(result, dict):
                    result["_performance"] = {
                        "response_time_ms": round(duration * 1000, 2),
                        "cached": False
                    }

                return result

            return await func(*args, **kwargs)

        return wrapper
    return decorator

# Funciones de utilidad para monitoreo
async def get_performance_stats() -> Dict[str, Any]:
    """
    Obtiene estadísticas de rendimiento del sistema.

    Returns:
        Diccionario con estadísticas
    """
    stats = {
        "system": performance_monitor.get_system_stats(),
        "endpoints": {}
    }

    # Estadísticas de endpoints
    for metric_name, durations in performance_monitor.metrics.items():
        if durations:
            stats["endpoints"][metric_name] = {
                "average_ms": round(performance_monitor.get_average(metric_name) * 1000, 2),
                "p95_ms": round((performance_monitor.get_percentile(metric_name, 95) or 0) * 1000, 2),
                "p99_ms": round((performance_monitor.get_percentile(metric_name, 99) or 0) * 1000, 2),
                "total_requests": len(durations)
            }

    return stats

def optimize_database_connection():
    """
    Optimiza la configuración de conexión a la base de datos.
    """
    # Configuraciones para mejorar rendimiento
    db_config = {
        "pool_pre_ping": True,  # Verificar conexiones antes de usar
        "pool_recycle": 3600,   # Reciclar conexiones cada hora
        "pool_size": 10,        # Tamaño del pool
        "max_overflow": 20,     # Máximo overflow
        "pool_timeout": 30,     # Timeout del pool
    }

    return db_config

# Funciones para optimización de memoria
def memory_efficient_iterator(items: List[Any], chunk_size: int = 100):
    """
    Iterador eficiente en memoria para procesar listas grandes.

    Args:
        items: Lista de items a procesar
        chunk_size: Tamaño del chunk

    Yields:
        Chunks de items
    """
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

async def async_batch_processor(items: List[Any], processor: Callable, batch_size: int = 10):
    """
    Procesador asíncrono por lotes para operaciones masivas.

    Args:
        items: Lista de items a procesar
        processor: Función procesadora
        batch_size: Tamaño del lote

    Returns:
        Lista de resultados
    """
    results = []
    for batch in memory_efficient_iterator(items, batch_size):
        batch_results = await asyncio.gather(*[processor(item) for item in batch])
        results.extend(batch_results)

    return results
