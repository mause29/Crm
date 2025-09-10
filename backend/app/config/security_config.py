"""
Security Configuration Module
Centralized security settings for the CRM application
"""
import os
from typing import List, Dict, Any

class SecurityConfig:
    """Security configuration class"""

    # JWT Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your-refresh-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Password Policy
    PASSWORD_MIN_LENGTH = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
    PASSWORD_REQUIRE_UPPERCASE = os.getenv("PASSWORD_REQUIRE_UPPERCASE", "true").lower() == "true"
    PASSWORD_REQUIRE_LOWERCASE = os.getenv("PASSWORD_REQUIRE_LOWERCASE", "true").lower() == "true"
    PASSWORD_REQUIRE_DIGITS = os.getenv("PASSWORD_REQUIRE_DIGITS", "true").lower() == "true"
    PASSWORD_REQUIRE_SPECIAL_CHARS = os.getenv("PASSWORD_REQUIRE_SPECIAL_CHARS", "true").lower() == "true"

    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE = int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "60"))
    RATE_LIMIT_EXCLUDE_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/health",
        "/favicon.ico"
    ]

    # CORS Settings
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    CORS_ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOWED_HEADERS = [
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "X-CSRF-Token"
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_MAX_AGE = 86400  # 24 hours

    # Security Headers
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        "X-Permitted-Cross-Domain-Policies": "none"
    }

    # File Upload Security
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "5242880"))  # 5MB
    ALLOWED_FILE_EXTENSIONS = [
        ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt"
    ]

    # Session Management
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    MAX_CONCURRENT_SESSIONS = int(os.getenv("MAX_CONCURRENT_SESSIONS", "5"))

    # Encryption
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "your-encryption-key-change-in-production")

    # Logging
    SECURITY_LOG_LEVEL = os.getenv("SECURITY_LOG_LEVEL", "INFO")
    LOG_SENSITIVE_DATA = os.getenv("LOG_SENSITIVE_DATA", "false").lower() == "true"

    # Feature Flags
    ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    ENABLE_XSS_PROTECTION = os.getenv("ENABLE_XSS_PROTECTION", "true").lower() == "true"
    ENABLE_SQL_INJECTION_PROTECTION = os.getenv("ENABLE_SQL_INJECTION_PROTECTION", "true").lower() == "true"
    ENABLE_CSRF_PROTECTION = os.getenv("ENABLE_CSRF_PROTECTION", "true").lower() == "true"
    ENABLE_SECURITY_HEADERS = os.getenv("ENABLE_SECURITY_HEADERS", "true").lower() == "true"
    ENABLE_INPUT_SANITIZATION = os.getenv("ENABLE_INPUT_SANITIZATION", "true").lower() == "true"

    @classmethod
    def get_password_policy(cls) -> Dict[str, Any]:
        """Get password policy configuration"""
        return {
            "min_length": cls.PASSWORD_MIN_LENGTH,
            "require_uppercase": cls.PASSWORD_REQUIRE_UPPERCASE,
            "require_lowercase": cls.PASSWORD_REQUIRE_LOWERCASE,
            "require_digits": cls.PASSWORD_REQUIRE_DIGITS,
            "require_special_chars": cls.PASSWORD_REQUIRE_SPECIAL_CHARS
        }

    @classmethod
    def get_cors_config(cls) -> Dict[str, Any]:
        """Get CORS configuration"""
        return {
            "allow_origins": cls.CORS_ALLOWED_ORIGINS,
            "allow_methods": cls.CORS_ALLOWED_METHODS,
            "allow_headers": cls.CORS_ALLOWED_HEADERS,
            "allow_credentials": cls.CORS_ALLOW_CREDENTIALS,
            "max_age": cls.CORS_MAX_AGE
        }

    @classmethod
    def get_rate_limit_config(cls) -> Dict[str, Any]:
        """Get rate limiting configuration"""
        return {
            "requests_per_minute": cls.RATE_LIMIT_REQUESTS_PER_MINUTE,
            "exclude_paths": cls.RATE_LIMIT_EXCLUDE_PATHS
        }

# Global security configuration instance
security_config = SecurityConfig()
