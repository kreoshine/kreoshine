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


class Base(DeclarativeBase):
    pass


class ClientRequest(Base):
    """
    Таблица карточек клиента.
    """
    __tablename__ = "client_request"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    mail: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    theme: Mapped[int] = mapped_column(ForeignKey("service.id"))
    status: Mapped[int] = mapped_column(
        ForeignKey("card_status.id"), default=1)
    executor: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class Users(Base):
    """
    Таблица пользователей/админов базы.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str]
    mail: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class Service(Base):
    """
    Таблица услуг.
    """
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[int] = mapped_column(
        ForeignKey("visible_status.id"), default=2)
    short_deskription: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class CardStatus(Base):
    """
    Таблица статусов карточки клиента.
    """
    __tablename__ = "card_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class VisibleStatus(Base):
    """
    Таблица статусов публикации.
    Услуга/новость будет показываться на сайте или нет в зависимости от статуса.
    """
    __tablename__ = "visible_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class Image(Base):
    """
    Единая таблица изобржений.
    """
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class News(Base):
    """
    Таблица новостей.
    """
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    heder: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[int] = mapped_column(
        ForeignKey("visible_status.id"), default=2)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class ServicesImg(Base):
    """
    Таблица привязки изображений к услугам.
    """
    __tablename__ = "services_img"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[str] = mapped_column(
        ForeignKey("service.id"), nullable=False)
    image_id: Mapped[str] = mapped_column(
        ForeignKey("image.id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())


class NewsImg(Base):
    """
    Таблица привязки изображений к новостям.
    """
    __tablename__ = "news_img"
    id: Mapped[int] = mapped_column(primary_key=True)
    news_id: Mapped[str] = mapped_column(ForeignKey("news.id"), nullable=False)
    image_id: Mapped[str] = mapped_column(
        ForeignKey("image.id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())
