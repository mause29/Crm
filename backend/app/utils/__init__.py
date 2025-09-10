# Utils package initialization
from ..models import LogAuditoria
from datetime import datetime

def log_accion(usuario: str, accion: str, db):
    """
    Registra una acción del usuario en el log de auditoría.

    Args:
        usuario (str): Email del usuario que realizó la acción
        accion (str): Descripción de la acción realizada
        db: Sesión de base de datos
    """
    try:
        log_entry = LogAuditoria(
            usuario=usuario,
            accion=accion,
            fecha=datetime.utcnow()
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        # Log the error but don't raise it to avoid breaking the main flow
        print(f"Error logging action: {e}")
        db.rollback()
