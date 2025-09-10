"""
API Monitoring Middleware
Tracks API calls and sends metrics to the monitoring service
"""
import time
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from ..services.monitoring_service import monitoring_service
from ..auth import get_current_user_optional
from ..database_new import get_db
from ..models import User
from sqlalchemy.orm import Session

class APIMonitoringMiddleware:
    """Middleware to monitor API calls and performance"""

    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # Create a custom ASGI app that wraps the original
        async def monitored_app(scope, receive, send):
            request = Request(scope, receive)

            # Skip monitoring for certain paths
            if self._should_skip_monitoring(request.url.path):
                return await self.app(scope, receive, send)

            start_time = time.time()
            user_id = None
            ip_address = self._get_client_ip(request)

            # Try to get user ID from JWT token (if available)
            try:
                # This is a simplified approach - in production you'd decode the JWT
                auth_header = request.headers.get("authorization", "")
                if auth_header.startswith("Bearer "):
                    token = auth_header[7:]
                    # You'd normally decode the token here to get user_id
                    # For now, we'll leave it as None or implement basic parsing
                    pass
            except:
                pass

            # Track the response
            original_send = send
            response_status = 200
            response_body = b""

            async def monitored_send(message):
                nonlocal response_status, response_body

                if message["type"] == "http.response.start":
                    response_status = message["status"]

                elif message["type"] == "http.response.body":
                    if not message.get("more_body", False):
                        response_body = message.get("body", b"")

                await original_send(message)

            try:
                # Process the request
                await self.app(scope, receive, monitored_send)

                # Calculate response time
                response_time = time.time() - start_time

                # Record the API call
                monitoring_service.record_api_call(
                    endpoint=request.url.path,
                    method=request.method,
                    response_time=response_time,
                    status_code=response_status,
                    user_id=user_id,
                    ip_address=ip_address
                )

            except Exception as e:
                # Record failed requests
                response_time = time.time() - start_time
                monitoring_service.record_api_call(
                    endpoint=request.url.path,
                    method=request.method,
                    response_time=response_time,
                    status_code=500,
                    user_id=user_id,
                    ip_address=ip_address
                )
                raise

        return await monitored_app(scope, receive, send)

    def _should_skip_monitoring(self, path: str) -> bool:
        """Check if path should be skipped from monitoring"""
        skip_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
            "/health",
            "/monitoring/health",
            "/performance/stats"
        ]

        # Skip static files and monitoring endpoints
        for skip_path in skip_paths:
            if path.startswith(skip_path):
                return True

        return False

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        # Check for forwarded headers first (behind proxy/load balancer)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Check for real IP header
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fall back to client IP from ASGI scope
        client = request.scope.get("client")
        if client:
            return client[0]

        return "unknown"

def add_api_monitoring_middleware(app):
    """Add API monitoring middleware to the FastAPI app"""
    app.add_middleware(APIMonitoringMiddleware)
    print("✅ API Monitoring middleware added")
