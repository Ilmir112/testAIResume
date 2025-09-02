import httpx
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.api.resumes.models import ResumesHistory
from app.api.resumes.schemas import SResumes
from app.config import settings
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_join(cls, model, filter_by: dict = None, join_related: str = None):
        async with async_session_maker() as session:
            query = select(model)
            if join_related:
                # Динамически применяем joinedload к отношению
                query = query.options(joinedload(getattr(model, join_related)))
            if filter_by:
                query = query.filter_by(**filter_by)
            result = await session.execute(query)
            if result:
                return result.unique().scalars().all()

    @classmethod
    async def add_with_history(cls, resume_data: SResumes, user_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                # Создаем резюме
                new_resume = cls.model(
                    title=resume_data.title,
                    context=resume_data.context,
                    user_id=user_id,
                )
                session.add(new_resume)
                await session.flush()  # чтобы получить id

                # Создаем историю
                new_history = ResumesHistory(
                    context=new_resume.context, resume_id=new_resume.id
                )
                session.add(new_history)

                try:
                    await session.commit()
                except SQLAlchemyError:
                    await session.rollback()
                    raise
                return new_resume

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(telegram_id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_applications(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.service))
                .filter_by(**filter_by)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def add_many(cls, instances: list[dict]):
        async with async_session_maker() as session:
            async with session.begin():
                new_instances = [cls.model(**values) for values in instances]
                session.add_all(new_instances)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instances

    @classmethod
    async def update(cls, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):

        async with async_session_maker() as session:
            async with session.begin():
                if delete_all:
                    query = select(cls.model)
                else:
                    query = select(cls.model).filter_by(**filter_by)

                result = await session.execute(query)
                objects = result.scalars().all()
                if not objects:
                    return 0

                for obj in objects:
                    await session.delete(obj)

                await session.commit()
                return len(objects)
