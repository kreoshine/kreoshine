# pylint: disable=E1102,R0903,E0213
""" Module contains models of the database tables in 'Declarative Style' """
from __future__ import annotations
import datetime
import uuid
from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """ Base class for models """
    type_annotation_map = {
        UUID: UUID,
    }

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), default=datetime.datetime.now())


class TradeItem(Base):
    """ Represents `trade items` table """
    __tablename__ = "trade_items"
    trade_item_uid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    description: Mapped[str]
    short_description: Mapped[str]
    is_visible: Mapped[bool] = mapped_column(default=False)


class User(Base):
    """ Represents `users` table """
    __tablename__ = "users"
    user_uid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    mail: Mapped[str]
    password_hash: Mapped[str]


class ClientRequest(Base):
    """ Represents `client requests` table """
    __tablename__ = "client_requests"
    client_request_uid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_name: Mapped[str]
    client_phone: Mapped[Optional[str]]
    client_mail: Mapped[str]
    message: Mapped[Optional[str]]
    tittle: Mapped[Optional[str]]
    request_status: Mapped[str] = mapped_column(default="received")
