from datetime import datetime

from pydantic import BaseModel, Field


class GetUserBalanceResponse(BaseModel):
    user_id: str
    balance: int

    class Config:
        orm_mode = True
