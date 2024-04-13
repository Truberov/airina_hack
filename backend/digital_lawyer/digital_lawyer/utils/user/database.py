from uuid import uuid4
import random

from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from balance.db.models import UserBalance


async def get_user(session: AsyncSession, user_id: str) -> UserBalance | None:
    query = select(UserBalance).where(UserBalance.user_id == user_id)
    return await session.scalar(query)


async def create_user(session: AsyncSession) -> [bool, str]:
    user = UserBalance(user_id=str(uuid4()), balance=random.randint(0, 1000000))
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False, ""
    return True, user
