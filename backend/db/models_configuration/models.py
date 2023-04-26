# pylint: disable=C0114,E1102,R0903
from __future__ import annotations
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
import enum
from sqlalchemy.dialects.postgresql import ENUM


class VisibleStatus(enum.Enum):
    visible = 'visible'
    invsible = 'invsible'


class Base(DeclarativeBase):
    def __tablename__(cls):
        return cls.__name__.lower()
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), default=datetime.datetime.now())


class Image(Base):
    """
    Единая таблица изобржений.
    """
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=False)


class Service(Base):
    """
    Таблица услуг.
    """
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    short_deskription: Mapped[str] = mapped_column(nullable=False)


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
    password_hash: Mapped[str]


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
    executor: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1)


class News(Base):
    """
    Таблица новостей.
    """
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)


if __name__ == "__main__":
    pass
