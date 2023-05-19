# pylint: disable=C0114,E1102,R0903, E0213
from __future__ import annotations
import datetime
from typing import Literal
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import sqlalchemy

Status = Literal["received", "discussed", "in progress", "closed"]
VStatus = Literal["visible", "invsible"]


class Base(DeclarativeBase):
    """
    Base class for the model
    """
    def __tablename__(cls):
        return cls.__name__.lower()
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), default=datetime.datetime.now())


class Service(Base):
    """
    Services table
    """
    __tablename__ = "service"
    service_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    short_desсription: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[VStatus] = mapped_column(sqlalchemy.Enum(
        "visible", "invsible", name="vstatus_enum"))


class Users(Base):
    """
    Table of database users/admins
    """
    __tablename__ = "users"

    users_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str]
    mail: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str]


class ClientRequest(Base):
    """
    Client card table
    """
    __tablename__ = "client_request"
    client_request_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    mail: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    theme: Mapped[int] = mapped_column(ForeignKey("service.id"))


if __name__ == "__main__":
    pass
