import pytz
from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from balance.db.models import ChangesHistory, UserBalance
from balance.schemas import ChangeBalanceRequest


async def get_last_balance_change(session: AsyncSession, user_id: str) -> datetime:
    query = select(ChangesHistory).where(ChangesHistory.user_id == user_id).order_by(
        ChangesHistory.operation_timestamp.desc())
    last_change = await session.scalar(query)

    timezone = pytz.timezone('Europe/Moscow')
    small_date = datetime(1900, 1, 1, tzinfo=timezone)

    return last_change.operation_timestamp if last_change else small_date


async def make_balance_change(session: AsyncSession, data: ChangeBalanceRequest, user) -> None:
    new_balance = user.balance + data.balance_change
    query = update(UserBalance).where(UserBalance.user_id == user.user_id).values(balance=new_balance)
    await session.execute(query)
    new_object = ChangesHistory(
        id=str(uuid4()),
        user_id=data.user_id,
        balance_change=data.balance_change,
        operation_timestamp=data.timestamp,
        context=data.context
    )
    session.add(new_object)
    await session.commit()
