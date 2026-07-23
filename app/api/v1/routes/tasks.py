"""
Task Management Endpoints
"""
import json
import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from app.schemas import TaskCreate, TaskRead, TaskUpdate, PaginatedResponse
from app.models import Task
from app.db import get_session, get_redis
from app.core.exceptions import NotFoundException
from app.core.config import settings

router = APIRouter(prefix="/tasks", tags=["Tasks"])


async def get_cache():
    return await get_redis()


@router.get("", response_model=PaginatedResponse)
async def list_tasks(
    session: AsyncSession = Depends(get_session),
    cache=Depends(get_cache),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    completed: bool | None = Query(None),
    priority: int | None = Query(None, ge=1, le=5),
) -> PaginatedResponse:
    cache_key = f"tasks:list:{page}:{page_size}:{completed}:{priority}"
    cached = await cache.get(cache_key)
    if cached:
        return PaginatedResponse(**json.loads(cached))

    offset = (page - 1) * page_size
    query = select(Task)
    if completed is not None:
        query = query.where(Task.completed == completed)
    if priority is not None:
        query = query.where(Task.priority == priority)

    query = query.offset(offset).limit(page_size).order_by(Task.created_at.desc())
    result = await session.execute(query)
    tasks = result.scalars().all()

    count_result = await session.execute(select(func.count(Task.id)))
    total = count_result.scalar() or 0

    response = PaginatedResponse(
        items=[TaskRead(**t.model_dump()).model_dump() for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total > 0 else 0,
        has_next=page * page_size < total,
        has_prev=page > 1
    )
    await cache.setex(cache_key, settings.cache_ttl, json.dumps(response.model_dump(), default=str))
    return response


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: str, session: AsyncSession = Depends(get_session), cache=Depends(get_cache)) -> TaskRead:
    cache_key = f"tasks:{task_id}"
    cached = await cache.get(cache_key)
    if cached:
        return TaskRead(**json.loads(cached))

    result = await session.get(Task, task_id)
    if not result:
        raise NotFoundException("Task not found")
    await cache.setex(cache_key, settings.cache_ttl, json.dumps(TaskRead(**result.model_dump()).model_dump(), default=str))
    return TaskRead(**result.model_dump())


@router.post("", response_model=TaskRead, status_code=201)
async def create_task(task_data: TaskCreate, session: AsyncSession = Depends(get_session), cache=Depends(get_cache), current_user: dict | None = None) -> TaskRead:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        completed=task_data.completed,
        user_id=current_user["sub"] if current_user else "anonymous",
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    await cache.delete("tasks:list:*")
    return TaskRead(**task.model_dump())


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(task_id: str, task_update: TaskUpdate, session: AsyncSession = Depends(get_session), cache=Depends(get_cache)) -> TaskRead:
    result = await session.get(Task, task_id)
    if not result:
        raise NotFoundException("Task not found")
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    await session.commit()
    await session.refresh(result)
    await cache.delete("tasks:list:*")
    return TaskRead(**result.model_dump())


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str, session: AsyncSession = Depends(get_session), cache=Depends(get_cache)):
    result = await session.get(Task, task_id)
    if not result:
        raise NotFoundException("Task not found")
    await session.delete(result)
    await session.commit()
    await cache.delete("tasks:list:*")