"""
Utilidades de seguridad para validación y sanitización de datos.
"""
import bleach
import html
import re
from typing import Dict, Any, List
from fastapi import UploadFile
import os

def sanitize_html(text: str) -> str:
    """
    Sanitiza HTML para prevenir XSS.

    Args:
        text: Texto HTML a sanitizar

    Returns:
        str: Texto sanitizado
    """
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'ul', 'ol', 'li']
    allowed_attrs = {}

    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs)

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitiza todas las entradas de texto en un diccionario.

    Args:
        data: Diccionario con datos a sanitizar

    Returns:
        Dict[str, Any]: Diccionario con datos sanitizados
    """
    sanitized = {}

    for key, value in data.items():
        if isinstance(value, str):
            # Escapar caracteres HTML
            sanitized[key] = html.escape(value.strip())
            # Sanitizar HTML si es necesario para campos de texto rico
            if key in ['description', 'notes', 'content', 'message']:
                sanitized[key] = sanitize_html(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_input(item) if isinstance(item, dict) else item for item in value]
        else:
            sanitized[key] = value

    return sanitized

def validate_file_upload(file: UploadFile, allowed_extensions: List[str], max_size: int = 5*1024*1024) -> UploadFile:
    """
    Valida un archivo subido.

    Args:
        file: Archivo a validar
        allowed_extensions: Extensiones permitidas
        max_size: Tamaño máximo en bytes

    Returns:
        UploadFile: Archivo validado

    Raises:
        ValueError: Si la validación falla
    """
    if not file:
        raise ValueError("No file provided")

    # Verificar extensión
    filename = file.filename.lower() if file.filename else ""
    if not any(filename.endswith(ext.lower()) for ext in allowed_extensions):
        raise ValueError(f"File type not allowed. Allowed: {', '.join(allowed_extensions)}")

    # Verificar tamaño
    file_content = file.file.read()
    if len(file_content) > max_size:
        raise ValueError(f"File too large. Max size: {max_size} bytes")

    # Reset file pointer
    file.file.seek(0)

    return file

def validate_email_domain(email: str, allowed_domains: List[str] = None) -> bool:
    """
    Valida el dominio de un email.

    Args:
        email: Email a validar
        allowed_domains: Lista de dominios permitidos (opcional)

    Returns:
        bool: True si el dominio es válido
    """
    if not allowed_domains:
        return True

    try:
        domain = email.split('@')[1].lower()
        return domain in [d.lower() for d in allowed_domains]
    except IndexError:
        return False

def validate_password_strength(password: str) -> Dict[str, bool]:
    """
    Valida la fortaleza de una contraseña.

    Args:
        password: Contraseña a validar

    Returns:
        Dict[str, bool]: Resultados de validación
    """
    checks = {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'lowercase': bool(re.search(r'[a-z]', password)),
        'digit': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[@$!%*?&]', password))
    }

    checks['overall'] = all(checks.values())
    return checks

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza un nombre de archivo para prevenir ataques de path traversal.

    Args:
        filename: Nombre de archivo original

    Returns:
        str: Nombre de archivo sanitizado
    """
    # Remover caracteres peligrosos
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)

    # Remover secuencias de puntos
    sanitized = re.sub(r'\.\.+', '.', sanitized)

    # Limitar longitud
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext

    return sanitized

def validate_sql_injection_safe(value: str) -> bool:
    """
    Verifica si un valor parece contener intentos de SQL injection.

    Args:
        value: Valor a verificar

    Returns:
        bool: True si parece seguro
    """
    sql_patterns = [
        r';\s*--',  # Comentarios SQL
        r';\s*/\*',  # Comentarios multilinea
        r'union\s+select',  # UNION SELECT
        r';\s*drop\s+table',  # DROP TABLE
        r';\s*delete\s+from',  # DELETE FROM
        r';\s*update.*set',  # UPDATE SET
        r';\s*insert\s+into',  # INSERT INTO
        r'--\s*$',  # Comentarios al final
        r'/\*.*\*/',  # Comentarios multilinea
    ]

    value_lower = value.lower()
    for pattern in sql_patterns:
        if re.search(pattern, value_lower, re.IGNORECASE):
            return False

    return True

def validate_xss_safe(value: str) -> bool:
    """
    Verifica si un valor parece contener intentos de XSS.

    Args:
        value: Valor a verificar

    Returns:
        bool: True si parece seguro
    """
    xss_patterns = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',  # JavaScript URLs
        r'on\w+\s*=',  # Event handlers
        r'<iframe[^>]*>.*?</iframe>',  # Iframe tags
        r'<object[^>]*>.*?</object>',  # Object tags
        r'<embed[^>]*>.*?</embed>',  # Embed tags
        r'expression\s*\(',  # CSS expressions
        r'vbscript:',  # VBScript
        r'data:text/html',  # Data URLs
    ]

    value_lower = value.lower()
    for pattern in xss_patterns:
        if re.search(pattern, value_lower, re.IGNORECASE):
            return False

    return True

def rate_limit_check(identifier: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
    """
    Verifica si una solicitud excede el límite de rate limiting.

    Nota: Esta es una implementación básica. Para producción,
    considera usar Redis u otra solución de cache distribuida.

    Args:
        identifier: Identificador único (ej: IP address)
        max_requests: Máximo número de requests permitidos
        window_seconds: Ventana de tiempo en segundos

    Returns:
        bool: True si está dentro del límite
    """
    # Esta es una implementación simplificada
    # En producción, usa Redis o similar
    import time
    from collections import defaultdict

    if not hasattr(rate_limit_check, '_requests'):
        rate_limit_check._requests = defaultdict(list)

    current_time = time.time()
    requests = rate_limit_check._requests[identifier]

    # Limpiar requests antiguos
    requests[:] = [req_time for req_time in requests if current_time - req_time < window_seconds]

    # Verificar límite
    if len(requests) >= max_requests:
        return False

    # Registrar request
    requests.append(current_time)
    return True

def log_security_event(event_type: str, details: Dict[str, Any], user_id: int = None, ip_address: str = None):
    """
    Registra un evento de seguridad.

    Args:
        event_type: Tipo de evento (ej: 'LOGIN_ATTEMPT', 'XSS_ATTEMPT')
        details: Detalles del evento
        user_id: ID del usuario involucrado (opcional)
        ip_address: Dirección IP del cliente (opcional)
    """
    import logging
    from datetime import datetime

    security_logger = logging.getLogger('security')

    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'ip_address': ip_address,
        'details': details
    }

    security_logger.warning(f"SECURITY_EVENT: {event_type} - {log_entry}")

def encrypt_sensitive_data(data: str) -> str:
    """
    Encripta datos sensibles usando Fernet.

    Args:
        data: Datos a encriptar

    Returns:
        str: Datos encriptados en base64
    """
    from cryptography.fernet import Fernet
    import base64

    # En producción, carga la clave desde variables de entorno
    key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
    if isinstance(key, str):
        key = key.encode()

    cipher = Fernet(key)
    encrypted = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """
    Desencripta datos sensibles.

    Args:
        encrypted_data: Datos encriptados en base64

    Returns:
        str: Datos desencriptados
    """
    from cryptography.fernet import Fernet
    import base64

    key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
    if isinstance(key, str):
        key = key.encode()

    cipher = Fernet(key)
    encrypted = base64.b64decode(encrypted_data)
    decrypted = cipher.decrypt(encrypted)
    return decrypted.decode()
