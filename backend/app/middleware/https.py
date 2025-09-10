"""
Middleware para soporte HTTPS y redirección HTTP a HTTPS.
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """
    Middleware que redirige todas las peticiones HTTP a HTTPS.
    Solo se activa en producción cuando se configura HTTPS.
    """

    def __init__(self, app, enable_redirect: bool = False, https_port: int = 443):
        super().__init__(app)
        self.enable_redirect = enable_redirect
        self.https_port = https_port

    async def dispatch(self, request: Request, call_next):
        # Solo redirigir si está habilitado y la petición es HTTP
        if self.enable_redirect and request.url.scheme == "http":
            # Construir URL HTTPS
            host = request.headers.get("host", "").split(":")[0]  # Remover puerto si existe
            https_url = f"https://{host}:{self.https_port}{request.url.path}"

            # Incluir query parameters si existen
            if request.url.query:
                https_url += f"?{request.url.query}"

            return RedirectResponse(
                url=https_url,
                status_code=status.HTTP_301_MOVED_PERMANENTLY
            )

        response = await call_next(request)
        return response

class HSTSHeaderMiddleware(BaseHTTPMiddleware):
    """
    Middleware que añade headers de seguridad HTTPS.
    """

    def __init__(self, app, enable_hsts: bool = True, hsts_max_age: int = 31536000):
        super().__init__(app)
        self.enable_hsts = enable_hsts
        self.hsts_max_age = hsts_max_age

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Solo añadir headers HSTS si la conexión es HTTPS
        if self.enable_hsts and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                f"max-age={self.hsts_max_age}; includeSubDomains; preload"
            )

        return response

class SSLRedirectMiddleware(BaseHTTPMiddleware):
    """
    Middleware avanzado para redirección SSL con configuración flexible.
    """

    def __init__(
        self,
        app,
        enable_redirect: bool = False,
        https_port: int = 443,
        exclude_paths: list = None,
        redirect_status_code: int = 301
    ):
        super().__init__(app)
        self.enable_redirect = enable_redirect
        self.https_port = https_port
        self.exclude_paths = exclude_paths or ["/health", "/.well-known"]
        self.redirect_status_code = redirect_status_code

    async def dispatch(self, request: Request, call_next):
        # Verificar si la petición debe ser excluida
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Redirigir HTTP a HTTPS si está habilitado
        if self.enable_redirect and request.url.scheme == "http":
            # Determinar el host correcto
            host = request.headers.get("host", "")
            if ":" in host:
                host = host.split(":")[0]  # Remover puerto HTTP

            # Construir URL HTTPS
            https_url = f"https://{host}"
            if self.https_port != 443:
                https_url += f":{self.https_port}"
            https_url += request.url.path

            # Añadir query parameters
            if request.url.query:
                https_url += f"?{request.url.query}"

            return RedirectResponse(
                url=https_url,
                status_code=self.redirect_status_code
            )

        response = await call_next(request)
        return response

# Función de configuración para añadir middleware HTTPS
def add_https_middleware(
    app,
    enable_redirect: bool = False,
    https_port: int = 443,
    enable_hsts: bool = True,
    hsts_max_age: int = 31536000,
    exclude_paths: list = None
):
    """
    Añade middleware HTTPS a la aplicación FastAPI.

    Args:
        app: Instancia de FastAPI
        enable_redirect: Si redirigir HTTP a HTTPS
        https_port: Puerto HTTPS (por defecto 443)
        enable_hsts: Si habilitar HSTS
        hsts_max_age: Tiempo máximo para HSTS en segundos
        exclude_paths: Rutas a excluir de la redirección
    """
    if enable_redirect:
        app.add_middleware(
            SSLRedirectMiddleware,
            enable_redirect=True,
            https_port=https_port,
            exclude_paths=exclude_paths
        )

    if enable_hsts:
        app.add_middleware(
            HSTSHeaderMiddleware,
            enable_hsts=True,
            hsts_max_age=hsts_max_age
        )
