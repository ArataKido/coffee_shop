from typing import Any, Generic, TypeVar

from sqlalchemy import select as sync_select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    """
    Generic repository for CRUD operations on models.
    """

    def __init__(self, db: AsyncSession | Session, model_class: type[T]):
        self.db = db
        self.model_class = model_class

    async def get_all(self) -> list[T]:
        """Get all records of the model."""
        result = await self.db.execute(select(self.model_class))
        return result.scalars().all()

    # TODO снести нахрен и заменить на find_by
    async def find_by_id(self, id: int) -> T | None:
        """Find a record by id, returns None if not found."""
        result = await self.db.execute(select(self.model_class).filter(self.model_class.id == id))
        return result.scalar_one_or_none()

    async def find_by(self, **kwargs) -> T | None:
        if not kwargs:
            raise ValueError("At least one search criteria must be provided.")

        filters = []

        for key, value in kwargs.items():
            if not hasattr(self.model_class, key):
                raise AttributeError(f"Field '{key}' does not exist on model '{self.model_class.__name__}'")
            if value is not None:
                filters.append(getattr(self.model_class, key) == value)

        if not filters:
            raise ValueError("Atl east one search value must be provided")
        query = select(self.model_class).filter(*filters)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def find_all(self) -> T | None:
        query = select(self.model_class)
        result = await self.db.execute(query)

        return result.scalars().all()

    async def find_all_by(self, **kwargs) -> T | None:
        if not kwargs:
            raise ValueError("At least one search criteria must be provided.")

        filters = []

        for key, value in kwargs.items():
            if not hasattr(self.model_class, key):
                raise AttributeError(f"Field '{key}' does not exist on model '{self.model_class.__name__}'")
            if value is not None:
                filters.append(getattr(self.model_class, key) == value)

        if not filters:
            raise ValueError("Atl east one search value must be provided")
        query = select(self.model_class).filter(*filters)
        result = await self.db.execute(query)

        return result.scalars().all()

    # Синхронная версия для Celery
    def find_by_sync(self, **kwargs) -> T | None:
        """Find a single record by any field(s) (sync version)."""
        filters = []
        for key, value in kwargs.items():
            if hasattr(self.model_class, key):
                filters.append(getattr(self.model_class, key) == value)

        result = self.db.execute(sync_select(self.model_class).filter(*filters))
        return result.scalar_one_or_none()

    def create_model(self, **data) -> T:
        """
        Factory method to create a model instance without saving to the database.
        This keeps model creation logic centralized and consistent.
        """
        return self.model_class(**data)

    async def add(self, model: T, created_by_user_id: int | None = None) -> T:
        """Add a model instance to the database."""
        if hasattr(model, "created_by") and created_by_user_id is not None:
            model.created_by = created_by_user_id

        self.db.add(model)
        await self.db.flush()  # Flush to get the ID without committing transaction
        return model

    async def add_and_commit(self, model: T, created_by_user_id: int | None = None) -> T:
        """Add a model instance and commit immediately."""
        model = await self.add(model, created_by_user_id)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def update(self, model: T, updated_by_user_id: int | None = None) -> T:
        """Update an existing model instance."""
        if hasattr(model, "updated_by") and updated_by_user_id is not None:
            model.updated_by = updated_by_user_id

        await self.db.flush()
        return model


    async def update_and_commit(self, model: T, updated_by_user_id: int | None = None) -> T:
        """Update a model instance and commit immediately."""
        model = await self.update(model, updated_by_user_id)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def soft_delete(self, model: T, deleted_by_user_id: int | None = None) -> T:
        """Soft delete a model by setting is_active to False."""
        if hasattr(model, "is_active"):
            model.is_active = False
            return await self.update(model, updated_by_user_id=deleted_by_user_id)
        return model

    async def activate(self, model: T, deleted_by_user_id: int | None = None) -> T:
        """Activating model by setting is_active to True."""
        if hasattr(model, "is_active"):
            model.is_active = True
            return await self.update(model, updated_by_user_id=deleted_by_user_id)
        return model

    async def permanent_delete(self, model_id: int) -> None:
        """Permanently delete a model by ID from the database."""
        model = await self.find_by_id(model_id)
        if model:
            await self.db.delete(model)
            await self.db.flush()

    # Синхронная версия для Celery
    def permanent_delete_sync(self, model_id: int) -> None:
        """Permanently delete a model by ID from the database (sync version)."""
        model = self.find_by_sync(id=model_id)
        if model:
            self.db.delete(model)
            self.db.flush()

    async def bulk_create(self, models: list[dict[str, Any]], created_by_user_id: int | None = None) -> list[T]:
        """Create multiple model instances at once."""
        instances = [self.create_model(**data) for data in models]

        if created_by_user_id is not None:
            for instance in instances:
                if hasattr(instance, "created_by"):
                    instance.created_by = created_by_user_id

        self.db.add_all(instances)
        await self.db.flush()
        return instances
