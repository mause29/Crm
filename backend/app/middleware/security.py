"""
Middleware de seguridad para la aplicación FastAPI.
Incluye rate limiting, headers de seguridad, CSRF protection y logging.
"""
import time
import re
from collections import defaultdict
from typing import Dict, List
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils.security import log_security_event

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para rate limiting basado en IP address.
    """

    def __init__(self, app, requests_per_minute: int = 60, exclude_paths: List[str] = None):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.exclude_paths = exclude_paths or ["/redoc", "/openapi.json"]
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Limpiar requests antiguos
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]

        # Verificar límite
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            log_security_event(
                "RATE_LIMIT_EXCEEDED",
                {"path": request.url.path, "method": request.method},
                ip_address=client_ip
            )
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many requests"}
            )

        # Registrar request
        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para añadir headers de seguridad HTTP completos.
    """

    def __init__(self, app, enable_hsts: bool = True, enable_csp: bool = True):
        super().__init__(app)
        self.enable_hsts = enable_hsts
        self.enable_csp = enable_csp

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Essential Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=(), usb=()"

        # HSTS (HTTP Strict Transport Security) - only for HTTPS
        if self.enable_hsts and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        # Content Security Policy
        if self.enable_csp:
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "media-src 'self'; "
                "object-src 'none'; "
                "frame-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'none';"
            )
            response.headers["Content-Security-Policy"] = csp

        # Additional Security Headers
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # Remove server information for security
        if "Server" in response.headers:
            del response.headers["Server"]

        if "X-Powered-By" in response.headers:
            del response.headers["X-Powered-By"]

        # Add security-related cache control
        if "Cache-Control" not in response.headers:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response

class SecurityLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging de eventos de seguridad.
    """

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "")
        path = request.url.path
        method = request.method

        # Log API access
        log_security_event(
            "API_ACCESS",
            {
                "method": method,
                "path": path,
                "user_agent": user_agent[:200]  # Limit user agent length
            },
            ip_address=client_ip
        )

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        # Log slow requests
        if duration > 5.0:  # More than 5 seconds
            log_security_event(
                "SLOW_REQUEST",
                {
                    "method": method,
                    "path": path,
                    "duration": duration,
                    "status_code": response.status_code
                },
                ip_address=client_ip
            )

        # Log error responses
        if response.status_code >= 400:
            log_security_event(
                "API_ERROR",
                {
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "duration": duration
                },
                ip_address=client_ip
            )

        return response

class XSSProtectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware básico para protección contra XSS.
    """

    def __init__(self, app):
        super().__init__(app)
        self.xss_patterns = [
            '<script[^>]*>.*?</script>',
            'javascript:',
            r'on\w+\s*=',
            '<iframe[^>]*>.*?</iframe>',
            '<object[^>]*>.*?</object>',
            '<embed[^>]*>.*?</embed>',
            'vbscript:',
            'data:text/html',
        ]

    async def dispatch(self, request: Request, call_next):
        # Check query parameters for XSS
        for param_name, param_value in request.query_params.items():
            if isinstance(param_value, str):
                for pattern in self.xss_patterns:
                    if pattern.lower() in param_value.lower():
                        client_ip = request.client.host if request.client else "unknown"
                        log_security_event(
                            "XSS_ATTEMPT_DETECTED",
                            {
                                "parameter": param_name,
                                "value": param_value[:100],  # Limit logged value
                                "pattern": pattern
                            },
                            ip_address=client_ip
                        )
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail": "Invalid request parameters"}
                        )

        response = await call_next(request)
        return response

class SQLInjectionProtectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware básico para protección contra SQL injection.
    """

    def __init__(self, app):
        super().__init__(app)
        self.sql_patterns = [
            r';\s*--',
            r';\s*/\*',
            r'union\s+select',
            r';\s*drop\s+table',
            r';\s*delete\s+from',
            r';\s*update.*set',
            r';\s*insert\s+into',
            r'--\s*$',
            r'/\*.*\*/',
        ]

    async def dispatch(self, request: Request, call_next):
        # Check query parameters for SQL injection
        for param_name, param_value in request.query_params.items():
            if isinstance(param_value, str):
                for pattern in self.sql_patterns:
                    if re.search(pattern, param_value, re.IGNORECASE):
                        client_ip = request.client.host if request.client else "unknown"
                        log_security_event(
                            "SQL_INJECTION_ATTEMPT_DETECTED",
                            {
                                "parameter": param_name,
                                "value": param_value[:100],  # Limit logged value
                                "pattern": pattern
                            },
                            ip_address=client_ip
                        )
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail": "Invalid request parameters"}
                        )

        response = await call_next(request)
        return response

class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware básico para protección CSRF.
    Requiere token CSRF para métodos que modifican datos.
    """

    def __init__(self, app, exempt_paths: List[str] = None):
        super().__init__(app)
        self.exempt_paths = exempt_paths or ["/users/token", "/docs", "/redoc"]

    async def dispatch(self, request: Request, call_next):
        # Skip CSRF check for safe methods and exempt paths
        if (request.method in ["GET", "HEAD", "OPTIONS"] or
            request.url.path in self.exempt_paths):
            return await call_next(request)

        # Check for CSRF token
        csrf_token = request.headers.get("X-CSRF-Token")
        if not csrf_token:
            client_ip = request.client.host if request.client else "unknown"
            log_security_event(
                "MISSING_CSRF_TOKEN",
                {"method": request.method, "path": request.url.path},
                ip_address=client_ip
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "CSRF token missing"}
            )

        # In a real implementation, you would validate the token
        # For now, just check if it's present and not empty
        if len(csrf_token.strip()) < 10:
            client_ip = request.client.host if request.client else "unknown"
            log_security_event(
                "INVALID_CSRF_TOKEN",
                {"method": request.method, "path": request.url.path},
                ip_address=client_ip
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid CSRF token"}
            )

        response = await call_next(request)
        return response

# Configuration function to add all security middleware
def add_security_middleware(app, config: Dict = None):
    """
    Añade todos los middleware de seguridad a la aplicación FastAPI.

    Args:
        app: Instancia de FastAPI
        config: Configuración opcional para los middleware
    """
    if config is None:
        config = {}

    # Rate limiting
    rate_limit_requests = config.get('rate_limit_requests', 60)
    exclude_paths = config.get('exclude_paths', ["/docs", "/redoc", "/openapi.json"])
    app.add_middleware(RateLimitMiddleware,
                      requests_per_minute=rate_limit_requests,
                      exclude_paths=exclude_paths)

    # Security headers
    app.add_middleware(SecurityHeadersMiddleware)

    # Security logging
    app.add_middleware(SecurityLoggingMiddleware)

    # XSS protection
    if config.get('enable_xss_protection', True):
        app.add_middleware(XSSProtectionMiddleware)

    # SQL injection protection
    if config.get('enable_sqli_protection', True):
        app.add_middleware(SQLInjectionProtectionMiddleware)

    # CSRF protection
    if config.get('enable_csrf_protection', True):
        csrf_exempt = config.get('csrf_exempt_paths', ["/users/token", "/docs", "/redoc"])
