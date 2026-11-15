
import os
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from pwdlib import PasswordHash
from dotenv import load_dotenv

# Password hashing using Argon2
password_hash = PasswordHash.recommended()


load_dotenv()
# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password before storing it."""
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Verify a password against its stored hash."""
    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict) -> str:
    """Generate a signed JWT access token."""

    if not SECRET_KEY:
        raise RuntimeError(
            "JWT_SECRET_KEY environment variable is not configured"
        )

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):
    """Decode and verify a JWT access token."""

    if not SECRET_KEY:
        raise RuntimeError(
            "JWT_SECRET_KEY environment variable is not configured"
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        return None
