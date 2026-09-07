from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from .config import settings


pwd_hasher = PasswordHash.recommended()


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_hasher.verify(
        plain_password,
        hashed_password,
    )


def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )