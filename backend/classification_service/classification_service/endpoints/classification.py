import random

from fastapi import APIRouter, Request, Body
from starlette import status

from classification_service.schemas import ClassifyDocumentRequest

api_router = APIRouter(tags=["classification"])

@api_router.post(
    "/classification",
    status_code=status.HTTP_200_OK,
)
async def get_answer(
        _: Request,
        body: ClassifyDocumentRequest = Body(...),
):
    data = ["statute", "order", "proxy", "contract", "act", "invoice", "bill", "contract offer", "determination",
              "application", "arrangement"]

    return random.choice(data)
