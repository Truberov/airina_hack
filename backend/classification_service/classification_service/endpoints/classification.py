import random

from fastapi import APIRouter, Request, Body, UploadFile
from starlette import status

from classification_service.utils.docs import parse_doc, get_doc_class
from classification_service.schemas import ClassifyDocumentRequest

api_router = APIRouter(tags=["classification"])


@api_router.post(
    "/classification",
    status_code=status.HTTP_200_OK,
)
async def get_answer(
        _: Request,
        file: UploadFile,
):
    content = await parse_doc(file)

    d_return = {
        "result": get_doc_class(content),
        "file": file.filename,
    }
    return d_return


@api_router.post(
    "/classification_by_text",
    status_code=status.HTTP_200_OK,
)
async def get_answer(
        _: Request,
        data: ClassifyDocumentRequest = Body(...),
):
    content = data.content

    d_return = {
        "result": get_doc_class(content),
    }
    return d_return
