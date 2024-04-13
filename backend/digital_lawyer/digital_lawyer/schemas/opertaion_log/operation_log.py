from pydantic import BaseModel
from typing import Optional


class OperationLog(BaseModel):
    status: str
    api_method: str
    data: Optional[dict]
    balance: Optional[int]
