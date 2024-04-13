import random
from datetime import datetime

import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status

from balance.schemas import ChangeBalanceRequest
from .database import get_last_balance_change, make_balance_change
from balance.utils.user import get_user
from balance.utils.operation_logs import write_operation_log
from balance.utils.approver import check_balance_changing
from balance.db.enums import ResultStatus
from balance.schemas import OperationLog


async def approve_balance_changing(
    session: AsyncSession,
    data_to_approve: ChangeBalanceRequest,
    api_method: str
) -> bool:
    verdict = True
    result_status = {False: ResultStatus.REJECTED, True: ResultStatus.ACCEPTED}
    last_change = await get_last_balance_change(session, data_to_approve.user_id)
    request_data = data_to_approve.dict()
    request_data["timestamp"] = request_data["timestamp"].isoformat()

    user = await get_user(session, user_id=data_to_approve.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    print(last_change, data_to_approve.timestamp, '##############################333')
    if last_change >= data_to_approve.timestamp or user.balance + data_to_approve.balance_change < 0:
        verdict = False

    elif abs(data_to_approve.balance_change) >= 100000:
        verdict = await check_balance_changing(
            user_id=data_to_approve.user_id,
            balance_change=data_to_approve.balance_change
        )

    data_for_log = OperationLog(
        api_method=api_method,
        data=request_data,
        status=result_status.get(verdict)
    )

    await write_operation_log(
        data_to_approve.timestamp,
        data_for_log.dict()
    )
    if verdict:
        await make_balance_change(session, data_to_approve, user)

    return verdict
