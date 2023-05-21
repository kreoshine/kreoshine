# pylint: disable=E1102,R0903,E0213
"""Module for creating a database model in Declarative Style"""
from __future__ import annotations
import datetime
from sqlalchemy import ForeignKey
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


class Service(Base):
    """
    Services table
    """
    __tablename__ = "service"
    service_id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    short_desсription: Mapped[str] = mapped_column(nullable=False)
    is_visible: Mapped[bool] = mapped_column(default=False)


class Users(Base):
    """
    Table of database users/admins
    """
    __tablename__ = "users"

    users_id: Mapped[int] = mapped_column(primary_key=True)
    users_first_name: Mapped[str] = mapped_column(nullable=False)
    users_last_name: Mapped[str]
    users_mail: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str]


class ClientRequest(Base):
    """
    Client card table
    valid values for request_status:
        "received", 
        "discussed", 
        "in progress", 
        "closed"
    """
    __tablename__ = "client_request"
    client_request_id: Mapped[int] = mapped_column(primary_key=True)
    client_name: Mapped[str] = mapped_column(nullable=False)
    client_phone: Mapped[str] = mapped_column(nullable=True)
    client_mail: Mapped[str] = mapped_column(nullable=False)
    client_message: Mapped[str] = mapped_column(nullable=False)
    theme: Mapped[int] = mapped_column(ForeignKey("service.service_id"))
    request_status: Mapped[str] = mapped_column(default="received")


if __name__ == "__main__":
    pass
