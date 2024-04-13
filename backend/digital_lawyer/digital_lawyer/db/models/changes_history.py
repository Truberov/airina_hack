# pylint: disable=E1102
from sqlalchemy import Column
from sqlalchemy import TIMESTAMP, UUID, BIGINT, VARCHAR, ForeignKey
from sqlalchemy.sql import func

from classification_service.db import DeclarativeBase


class ChangesHistory(DeclarativeBase):
    __tablename__ = "changes_history"

    id = Column(
        VARCHAR(50),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique index of element",
    )
    user_id = Column(
        ForeignKey("user_balance.user_id"),
        nullable=False,
        doc="Identifier of user",
    )
    balance_change = Column(
        BIGINT,
        nullable=False,
        doc="balance change of user",
    )
    operation_timestamp = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        doc="Date and time of operation",
    )
    context = Column(
        VARCHAR(100),
        nullable=True,
        doc="context of operation"
    )
