from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
import sys
import logging
from .database_new import get_db
from .models import User

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    
    sys.exit("SECRET_KEY environment variable is required for security.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token for user authentication.

    Args:
        data: Dictionary containing user data (typically email as 'sub' claim)
        expires_delta: Optional custom expiration time delta

    Returns:
        str: Encoded JWT token string
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()

    # Set token expiration time - use provided delta or default to 30 minutes
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiration claim to the JWT payload
    to_encode.update({"exp": expire})

    # Encode the payload into a JWT token using HS256 algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verify and decode a JWT token to extract user email.

    Args:
        token: JWT token string from Authorization header

    Returns:
        str: User email extracted from token

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode the JWT token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the subject (user email) from the payload
        email: str = payload.get("sub")

        # Validate that email exists in the payload
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        # Handle invalid, expired, or malformed tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    FastAPI dependency to get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session dependency

    Returns:
        User: Current authenticated user object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Extract email from JWT token
    email = verify_token(credentials.credentials)

    # Query user from database by email
    user = db.query(User).filter(User.email == email).first()

    # Validate that user exists in database
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    FastAPI dependency to ensure the current user is active.

    Args:
        current_user: User object from get_current_user dependency

    Returns:
        User: Active user object

    Raises:
        HTTPException: If user account is inactive
    """
    # Check if user account is active
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
