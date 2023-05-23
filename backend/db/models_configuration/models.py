# pylint: disable=E1102,R0903,E0213
"""Module for creating a database model in Declarative Style"""
from __future__ import annotations
import datetime
from uuid import uuid4
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """
    Base class for the model
    """
    def __tablename__(cls):
        return cls.__name__.lower()
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), default=datetime.datetime.now())


class TradeItem(Base):
    """
    Services table
    """
    __tablename__ = "trade_items"
    trade_items_uid: Mapped[str] = mapped_column(
        default=uuid4, primary_key=True, unique=True)
    trade_items_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    short_desсription: Mapped[str] = mapped_column(nullable=False)
    is_visible: Mapped[bool] = mapped_column(default=False)


class User(Base):
    """
    Table of database users/admins
    """
    __tablename__ = "users"
    user_uid: Mapped[str] = mapped_column(
        default=uuid4, primary_key=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str]
    mail: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str]


class ClientRequest(Base):
    """
    Client card table
    """
    __tablename__ = "client_requests"
    client_request_uid: Mapped[str] = mapped_column(
        default=uuid4, primary_key=True, unique=True)
    client_name: Mapped[str] = mapped_column(nullable=False)
    client_phone: Mapped[str] = mapped_column(nullable=True)
    client_mail: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    tittle: Mapped[str]
    request_status: Mapped[str] = mapped_column(default="received")


if __name__ == "__main__":
    pass
