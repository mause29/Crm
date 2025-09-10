"""
Security Headers Middleware for FastAPI

This middleware adds essential security headers to all HTTP responses
to protect against common web vulnerabilities.
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from typing import Callable
import time
from ..utils.cache import cache_manager

class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to all responses.

    This middleware implements OWASP security headers recommendations
    to protect against common web vulnerabilities.
    """

    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Process the request
        start_time = time.time()

        async def send_with_security_headers(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))

                # Add security headers
                security_headers = self._get_security_headers()

                # Convert headers to list of tuples if needed
                if isinstance(headers, dict):
                    headers_list = []
                    for key, value in headers.items():
                        # key and value might already be bytes, so check before encoding
                        if isinstance(key, bytes):
                            encoded_key = key
                        else:
                            encoded_key = key.encode()
                        if isinstance(value, bytes):
                            encoded_value = value
                        else:
                            encoded_value = value.encode()
                        headers_list.append([encoded_key, encoded_value])
                    headers = headers_list

                # Add security headers
                for header_name, header_value in security_headers.items():
                    # header_name and header_value are str, encode to bytes
                    headers.append([header_name.encode(), header_value.encode()])
                        
                message["headers"] = headers

            await send(message)

        await self.app(scope, receive, send_with_security_headers)

    def _get_security_headers(self) -> dict:
        """
        Get all security headers to be added to responses.

        Returns:
            dict: Dictionary of security headers and their values
        """
        headers = {}

        # Content Security Policy (CSP)
        headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )

        # HTTP Strict Transport Security (HSTS)
        headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        # X-Frame-Options
        headers["X-Frame-Options"] = "DENY"

        # X-Content-Type-Options
        headers["X-Content-Type-Options"] = "nosniff"

        # X-XSS-Protection
        headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer-Policy
        headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions-Policy (formerly Feature-Policy)
        headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), "
            "payment=(), usb=(), magnetometer=()"
        )

        # Cross-Origin Embedder Policy
        headers["Cross-Origin-Embedder-Policy"] = "require-corp"

        # Cross-Origin Opener Policy
        headers["Cross-Origin-Opener-Policy"] = "same-origin"

        # Cross-Origin Resource Policy
        headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # Remove server information
        headers["X-Powered-By"] = ""

        return headers

def add_security_headers(response: Response) -> Response:
    """
    Add security headers to a FastAPI response object.

    This function can be used as a dependency or decorator
    to add security headers to specific endpoints.

    Args:
        response: FastAPI Response object

    Returns:
        Response: Response with security headers added
    """
    security_headers = SecurityHeadersMiddleware(None)._get_security_headers()

    for header_name, header_value in security_headers.items():
        response.headers[header_name] = header_value

    return response

# Rate limiting functionality
class RateLimiter:
    """
    Simple rate limiter using async cache.

    This is a basic implementation. For production use,
    consider using Redis or a dedicated rate limiting service.
    """

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.cache_prefix = "rate_limit:"

    async def is_rate_limited(self, client_ip: str) -> bool:
        """
        Check if client is rate limited.

        Args:
            client_ip: Client IP address

        Returns:
            bool: True if rate limited, False otherwise
        """
        cache_key = f"{self.cache_prefix}{client_ip}"
        current_time = int(time.time())

        # Get current request count for this minute
        request_data = await cache_manager.get(cache_key)
        if request_data:
            count, window_start = request_data
            # Check if we're in the same minute window
            if current_time - window_start < 60:
                if count >= self.requests_per_minute:
                    return True
                count += 1
            else:
                # New minute window
                count = 1
                window_start = current_time
        else:
            count = 1
            window_start = current_time

        # Update cache
        await cache_manager.set(cache_key, (count, window_start), ttl_seconds=60)
        return False

async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware for FastAPI.

    This middleware checks if the client has exceeded the rate limit
    and returns a 429 status code if so.

    Args:
        request: FastAPI Request object
        call_next: Next middleware/route handler

    Returns:
        Response: Either the normal response or a 429 error
    """
    client_ip = request.client.host if request.client else "unknown"
    limiter = RateLimiter()

    if await limiter.is_rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too Many Requests",
                "message": "Rate limit exceeded. Please try again later.",
                "retry_after": 60
            },
            headers={"Retry-After": "60"}
        )

    response = await call_next(request)
    return response
