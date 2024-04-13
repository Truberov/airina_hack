import random

from fastapi import APIRouter, Request, Body, UploadFile
from starlette import status

from classification_service.utils.docs import parse_doc

api_router = APIRouter(tags=["classification"])


@api_router.post(
    "/classification",
    status_code=status.HTTP_200_OK,
)
async def get_answer(
        _: Request,
        file: UploadFile,
):

    data = ["statute", "order", "proxy", "contract", "act", "invoice", "bill", "contract offer", "determination",
            "application", "arrangement"]
    d_return = {
        "result": random.choice(data),
        "file": file.filename,
    }
    return d_return
