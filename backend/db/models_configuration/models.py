# pylint: disable=E1102,R0903,E0213
"""Module for creating a database model in Declarative Style"""
from __future__ import annotations
import datetime
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class Base(DeclarativeBase):
    """
    Base class for the model
    """
    type_annotation_map = {
        uuid.UUID: GUID,
    }

    def __tablename__(cls):
        return cls.__name__.lower()
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), default=datetime.datetime.now())


class TradeItem(Base):
    """
    Trade Items table
    """
    __tablename__ = "trade_items"
    trade_item_uid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    short_description: Mapped[str] = mapped_column(nullable=False)
    is_visible: Mapped[bool] = mapped_column(default=False)


class User(Base):
    """
    Table of database users/admins
    """
    __tablename__ = "users"
    user_uid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str]
    mail: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str]


class ClientRequest(Base):
    """
    Client card table
    """
    __tablename__ = "client_requests"
    client_request_uid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    client_name: Mapped[str] = mapped_column(nullable=False)
    client_phone: Mapped[str] = mapped_column(nullable=True)
    client_mail: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    tittle: Mapped[str]
    request_status: Mapped[str] = mapped_column(default="received")


if __name__ == "__main__":
    pass
