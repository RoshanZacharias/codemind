from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import AsyncSessionLocal
from .models.user import User


security = HTTPBearer()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        user_id = int(user_id)

    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user