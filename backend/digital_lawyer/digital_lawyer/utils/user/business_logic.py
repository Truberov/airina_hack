from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .database import get_user
from balance.db.models import UserBalance
from balance.utils.operation_logs import write_operation_log
from balance.db.enums import ResultStatus
from balance.schemas import OperationLog


async def get_user_balance(session: AsyncSession, user_id: str, timestamp: datetime, api_method) -> UserBalance:
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find user"
    )

    user = await get_user(session=session, user_id=user_id)
    if not user:
        raise user_not_found_exception

    data_for_log = OperationLog(
        api_method=str(api_method),
        balance=user.balance,
        status=ResultStatus.ACCEPTED
    )
    await write_operation_log(
        timestamp,
        data_for_log.dict()
    )

    return user
