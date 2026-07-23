"""
User Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.schemas import UserRead, UserCreate
from app.models import User
from app.db import get_session
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[UserRead]:
    result = await session.execute(select(User).offset(skip).limit(limit).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [UserRead(**u.model_dump()) for u in users]


@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: dict = Depends(lambda: {"id": "x", "name": "x", "email": "x"})) -> UserRead:
    return UserRead(**current_user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: str, session: AsyncSession = Depends(get_session)) -> UserRead:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead(**user.model_dump())


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:
    result = await session.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        hashed_password=hash_password(user_data.password),
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead(**user.model_dump())


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: str, user_update: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return UserRead(**user.model_dump())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await session.delete(user)
    await session.commit()