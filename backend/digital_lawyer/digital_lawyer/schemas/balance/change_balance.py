from datetime import datetime

from pydantic import BaseModel, Field


class ChangeBalanceRequest(BaseModel):
    user_id: str = Field(..., alias="userId")
    context: str
    balance_change: int = Field(..., alias="balanceChange")
    timestamp: datetime
