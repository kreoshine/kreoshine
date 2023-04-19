from __future__ import annotations

import asyncio
import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from models import Base, ClientRequest, Users, Service, CardStatus, VisibleStatus, Image, News, ServicesImg, NewsImg

DATABASE_URL = "postgresql+asyncpg://pguser:tr134sdfWE@localhost/postgres_ql"


async def insert_objects(async_session: async_sessionmaker[AsyncSession]) -> None:

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    # 1--------------------------
                    # VisibleStatus(name="visible"),
                    # VisibleStatus(name="invisible"),
                    # CardStatus(name="received"),
                    # CardStatus(name="discussed"),
                    # CardStatus(name="in progress"),
                    # CardStatus(name="closed"),
                    # 2--------------------------
                    # Service(name="Объемные световые буквы",
                    #         description="Объемные световые буквы", status=2,
                    #         short_deskription="Объемные световые буквы"),
                    # Service(name="Вывеска из гибкого неона",
                    #         description="Вывеска из гибкого неона", status=2,
                    #         short_deskription="Вывеска из гибкого неона"),
                    # Service(name="Дизайн проект вывески",
                    #         description="Дизайн проект вывески", status=2,
                    #         short_deskription="Дизайн проект вывески"),
                    # Service(name="Наклейки", description="Наклейки",
                    #         status=2, short_deskription="Наклейки"),
                    # Service(name="Таблички", description="Таблички",
                    #         status=2, short_deskription="Таблички"),
                    # Service(name="Визитки", description="Визитки",
                    #         status=2, short_deskription="Визитки"),
                    # Service(name="Лазерная печать", description="Лазерная печать", status=2,
                    #         short_deskription="Лазерная печать"),
                    # Service(name="Листовки", description="Листовки",
                    #         status=2, short_deskription="Листовки"),
                    # Service(name="Псевдообъемные вывески",
                    #         description="Псевдообъемные вывески", status=2,
                    #         short_deskription="Псевдообъемные вывески"),
                    # Service(name="Объемные световые буквы",
                    #         description="Объемные световые буквы", status=2,
                    #         short_deskription="Объемные световые буквы"),
                    # 3--------------------------
                    #  Users(first_name="Иван", last_name="Кузнецов",
                    #       mail="blacksmith@gmail.com", password_hash='none'),
                    # 4--------------------------
                    # ClientRequest(name="Иван", phone="+8(905)2349021", mail='bigboss@gmail.com',
                    #               message="Есть желание пообщаться по поводу визиток, нужно 1000 штук, тиснение",
                    #               theme=6, status=1, executor=1)

                ]
            )


# async def select_and_update_objects(
        # async_session: async_sessionmaker[AsyncSession],) -> None:

    # async with async_session() as session:
        # ...


async def async_main() -> None:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await insert_objects(async_session)
    # await select_and_update_objects(async_session)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


asyncio.run(async_main())
