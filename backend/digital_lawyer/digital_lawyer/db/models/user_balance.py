# pylint: disable=E1102
from sqlalchemy import Column
from sqlalchemy import TIMESTAMP, UUID, BIGINT, VARCHAR
from sqlalchemy.sql import func

from classification_service.db import DeclarativeBase


class UserBalance(DeclarativeBase):
    __tablename__ = "user_balance"

    user_id = Column(
        VARCHAR(50),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique index of element (type UUID)",
    )
    balance = Column(
        BIGINT,
        nullable=False,
        doc="balance of user",
    )
