"""
Sistema de caché para optimización de rendimiento.
Soporta caché en memoria y Redis.
"""
import json
import hashlib
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import asyncio
from functools import wraps
import redis.asyncio as redis
from ..config.settings import settings

class CacheManager:
    """
    Gestor de caché unificado que soporta múltiples backends.
    """

    def __init__(self):
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.redis_client: Optional[redis.Redis] = None

        # Inicializar Redis si está configurado
        if settings.REDIS_URL:
            try:
                self.redis_client = redis.from_url(settings.REDIS_URL)
            except Exception as e:
                print(f"Redis connection failed: {e}")
                self.redis_client = None

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Genera una clave única para el caché basada en los argumentos."""
        key_data = {
            "prefix": prefix,
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché."""
        # Intentar Redis primero
        if self.redis_client:
            try:
                cached_data = await self.redis_client.get(key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Redis get error: {e}")

        # Fallback a caché en memoria
        if key in self.memory_cache:
            cache_entry = self.memory_cache[key]
            if cache_entry["expires_at"] > datetime.utcnow():
                return cache_entry["data"]
            else:
                # Eliminar entrada expirada
                del self.memory_cache[key]

        return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Almacena un valor en el caché."""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

        # Intentar Redis primero
        if self.redis_client:
            try:
                await self.redis_client.setex(key, ttl_seconds, json.dumps(value, default=str))
                return
            except Exception as e:
                print(f"Redis set error: {e}")

        # Fallback a caché en memoria
        self.memory_cache[key] = {
            "data": value,
            "expires_at": expires_at
        }

    async def delete(self, key: str) -> None:
        """Elimina un valor del caché."""
        # Intentar Redis primero
        if self.redis_client:
            try:
                await self.redis_client.delete(key)
            except Exception as e:
                print(f"Redis delete error: {e}")

        # Eliminar de caché en memoria
        if key in self.memory_cache:
            del self.memory_cache[key]

    async def clear_pattern(self, pattern: str) -> None:
        """Elimina todas las claves que coinciden con un patrón."""
        # Para Redis
        if self.redis_client:
            try:
                keys = await self.redis_client.keys(pattern)
                if keys:
                    await self.redis_client.delete(*keys)
            except Exception as e:
                print(f"Redis clear pattern error: {e}")

        # Para caché en memoria (menos eficiente)
        keys_to_delete = [k for k in self.memory_cache.keys() if pattern.replace("*", "") in k]
        for key in keys_to_delete:
            del self.memory_cache[key]

    async def clear_all(self) -> None:
        """Limpia todo el caché."""
        # Redis
        if self.redis_client:
            try:
                await self.redis_client.flushdb()
            except Exception as e:
                print(f"Redis clear all error: {e}")

        # Memoria
        self.memory_cache.clear()

# Instancia global del gestor de caché
cache_manager = CacheManager()

def cached(ttl_seconds: int = 300, key_prefix: str = ""):
    """
    Decorador para cachear resultados de funciones asíncronas.

    Args:
        ttl_seconds: Tiempo de vida en segundos
        key_prefix: Prefijo para la clave del caché
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generar clave única
            cache_key = cache_manager._generate_key(key_prefix or func.__name__, *args, **kwargs)

            # Intentar obtener del caché
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Ejecutar función y cachear resultado
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, ttl_seconds)

            return result

        return wrapper
    return decorator

def invalidate_cache(pattern: str):
    """
    Decorador para invalidar caché después de ejecutar una función.

    Args:
        pattern: Patrón de claves a invalidar
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            # Invalidar caché después de la ejecución
            await cache_manager.clear_pattern(pattern)
            return result

        return wrapper
    return decorator

class PaginationParams:
    """Parámetros de paginación estándar."""

    def __init__(self, page: int = 1, per_page: int = 10, max_per_page: int = 100):
        self.page = max(1, page)
        self.per_page = min(max(1, per_page), max_per_page)
        self.offset = (self.page - 1) * self.per_page

class PaginatedResponse:
    """Respuesta paginada estándar."""

    def __init__(self, items: List[Any], total: int, page: int, per_page: int):
        self.items = items
        self.total = total
        self.page = page
        self.per_page = per_page
        self.total_pages = (total + per_page - 1) // per_page
        self.has_next = page < self.total_pages
        self.has_prev = page > 1

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la respuesta a diccionario."""
        return {
            "items": self.items,
            "pagination": {
                "page": self.page,
                "per_page": self.per_page,
                "total": self.total,
                "total_pages": self.total_pages,
                "has_next": self.has_next,
                "has_prev": self.has_prev
            }
        }

# Funciones de utilidad para caché
async def get_cached_user_list(company_id: int, page: int = 1, per_page: int = 10) -> Optional[Dict]:
    """Obtiene lista de usuarios cacheada."""
    cache_key = f"user_list:company_{company_id}:page_{page}:per_page_{per_page}"
    return await cache_manager.get(cache_key)

async def set_cached_user_list(company_id: int, page: int, per_page: int, data: Dict, ttl: int = 300) -> None:
    """Cachea lista de usuarios."""
    cache_key = f"user_list:company_{company_id}:page_{page}:per_page_{per_page}"
    await cache_manager.set(cache_key, data, ttl)

async def invalidate_user_cache(company_id: int) -> None:
    """Invalida caché de usuarios para una compañía."""
    pattern = f"user_list:company_{company_id}:*"
    await cache_manager.clear_pattern(pattern)

async def get_cached_client_list(company_id: int, page: int = 1, per_page: int = 10) -> Optional[Dict]:
    """Obtiene lista de clientes cacheada."""
    cache_key = f"client_list:company_{company_id}:page_{page}:per_page_{per_page}"
    return await cache_manager.get(cache_key)

async def set_cached_client_list(company_id: int, page: int, per_page: int, data: Dict, ttl: int = 300) -> None:
    """Cachea lista de clientes."""
    cache_key = f"client_list:company_{company_id}:page_{page}:per_page_{per_page}"
    await cache_manager.set(cache_key, data, ttl)

async def invalidate_client_cache(company_id: int) -> None:
    """Invalida caché de clientes para una compañía."""
    pattern = f"client_list:company_{company_id}:*"
    await cache_manager.clear_pattern(pattern)
