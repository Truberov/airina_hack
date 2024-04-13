from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from classification_service.db.connection import get_session
from classification_service.schemas import GetUserBalanceResponse, ChangeBalanceRequest

from classification_service.utils.balance import approve_balance_changing
from classification_service.utils.user import create_user, get_user_balance

api_router = APIRouter(
    tags=["User Balance Operations"],
)


@api_router.post(
    "/changeBalance",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Could not approve change",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Could not find user",
        },
    },
)
async def change_user_balance(
    request: Request,
    data_to_approve: ChangeBalanceRequest,
    session: AsyncSession = Depends(get_session),
):
    verdict = await approve_balance_changing(session, data_to_approve, request.url.path)
    if not verdict:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not approve change"
        )
    return Response(status_code=200)


@api_router.get(
    "/{user_id:str}/balance",
    status_code=status.HTTP_200_OK,
    response_model=GetUserBalanceResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Could not find user",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Could not get user balance with current timestamp"
        },
    },
)
async def check_user_balance(
    request: Request,
    user_id: str,
    timestamp: datetime,
    session: AsyncSession = Depends(get_session),

):
    user_info = await get_user_balance(session, user_id, timestamp, request.url.path)
    return GetUserBalanceResponse(
        user_id=user_info.user_id,
        balance=user_info.balance
    )


@api_router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Could not approve change",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Could not find user",
        },
    },
)
async def create_random_user(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    verdict, user = await create_user(session)
    if not verdict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT
        )
    return {"user_id": user.user_id, "balance": user.balance}
