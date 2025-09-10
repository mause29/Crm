"""
Session Management Module
Handles user sessions, concurrent session limits, and session security
"""
import time
import secrets
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
from ..config.security_config import security_config

@dataclass
class Session:
    """Session data structure"""
    session_id: str
    user_id: int
    email: str
    created_at: datetime
    last_activity: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True

class SessionManager:
    """Thread-safe session manager"""

    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        self._user_sessions: Dict[int, List[str]] = {}
        self._lock = threading.Lock()
        self._cleanup_thread = None
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        """Start background thread for session cleanup"""
        def cleanup_worker():
            while True:
                time.sleep(300)  # Run every 5 minutes
                self._cleanup_expired_sessions()

        self._cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        self._cleanup_thread.start()

    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        with self._lock:
            current_time = datetime.utcnow()
            expired_sessions = []

            for session_id, session in self._sessions.items():
                if (current_time - session.last_activity).total_seconds() > (security_config.SESSION_TIMEOUT_MINUTES * 60):
                    expired_sessions.append(session_id)
                    session.is_active = False

            for session_id in expired_sessions:
                self._remove_session(session_id)

    def create_session(self, user_id: int, email: str, ip_address: str, user_agent: str) -> str:
        """Create a new session for user"""
        with self._lock:
            # Check concurrent session limit
            user_sessions = self._user_sessions.get(user_id, [])
            if len(user_sessions) >= security_config.MAX_CONCURRENT_SESSIONS:
                # Remove oldest session
                oldest_session_id = user_sessions[0]
                self._remove_session(oldest_session_id)

            # Create new session
            session_id = secrets.token_urlsafe(32)
            session = Session(
                session_id=session_id,
                user_id=user_id,
                email=email,
                created_at=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                ip_address=ip_address,
                user_agent=user_agent
            )

            self._sessions[session_id] = session
            if user_id not in self._user_sessions:
                self._user_sessions[user_id] = []
            self._user_sessions[user_id].append(session_id)

            return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        with self._lock:
            session = self._sessions.get(session_id)
            if session and session.is_active:
                # Update last activity
                session.last_activity = datetime.utcnow()
                return session
            return None

    def validate_session(self, session_id: str, user_id: int) -> bool:
        """Validate if session is active and belongs to user"""
        session = self.get_session(session_id)
        return session is not None and session.user_id == user_id and session.is_active

    def invalidate_session(self, session_id: str):
        """Invalidate a specific session"""
        with self._lock:
            self._remove_session(session_id)

    def invalidate_user_sessions(self, user_id: int):
        """Invalidate all sessions for a user"""
        with self._lock:
            if user_id in self._user_sessions:
                session_ids = self._user_sessions[user_id].copy()
                for session_id in session_ids:
                    self._remove_session(session_id)

    def _remove_session(self, session_id: str):
        """Remove session from all data structures"""
        if session_id in self._sessions:
            session = self._sessions[session_id]
            user_id = session.user_id

            # Remove from sessions dict
            del self._sessions[session_id]

            # Remove from user sessions list
            if user_id in self._user_sessions:
                if session_id in self._user_sessions[user_id]:
                    self._user_sessions[user_id].remove(session_id)
                if not self._user_sessions[user_id]:
                    del self._user_sessions[user_id]

    def get_active_sessions_count(self, user_id: int) -> int:
        """Get number of active sessions for user"""
        with self._lock:
            return len(self._user_sessions.get(user_id, []))

    def get_session_info(self, user_id: int) -> List[Dict]:
        """Get information about user's active sessions"""
        with self._lock:
            session_info = []
            if user_id in self._user_sessions:
                for session_id in self._user_sessions[user_id]:
                    if session_id in self._sessions:
                        session = self._sessions[session_id]
                        session_info.append({
                            "session_id": session.session_id,
                            "created_at": session.created_at.isoformat(),
                            "last_activity": session.last_activity.isoformat(),
                            "ip_address": session.ip_address,
                            "user_agent": session.user_agent[:100]  # Truncate for security
                        })
            return session_info

# Global session manager instance
session_manager = SessionManager()
