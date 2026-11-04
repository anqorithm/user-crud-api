from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get(self, id: str) -> T | None:
        return await self.session.get(self.model, id)

    async def get_by_email(self, email: str) -> T | None:
        result = await self.session.execute(select(self.model).where(self.model.email == email))  # type: ignore[attr-defined]
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        result = await self.session.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: T) -> T:
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: str) -> bool:
        obj = await self.session.get(self.model, id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

    async def count(self) -> int:
        result = await self.session.execute(select(self.model))
        return len(list(result.scalars().all()))


from app.models.user_task import User  # noqa: E402

UserRepo = BaseRepository[User]
