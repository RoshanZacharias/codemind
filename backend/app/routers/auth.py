from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import AsyncSessionLocal
from ..models.user import User
from ..schemas.auth import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from ..security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }