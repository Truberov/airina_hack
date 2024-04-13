from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Request, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from bookmarker.db.connection import get_session
from bookmarker.db.enums import BookmarksSortKey
from bookmarker.db.models import User
from bookmarker.schemas import Bookmark as BookmarkSchema
from bookmarker.schemas import BookmarkCreateRequest
from bookmarker.utils import bookmark as utils
from bookmarker.utils.user import get_current_user


api_router = APIRouter(
    tags=["Documents"],
)


@api_router.post(
    "docs",
    status_code=status.HTTP_201_CREATED,
    response_model=BookmarkSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def create(
    _: Request,
    bookmark_instance: BookmarkCreateRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    title = utils.get_page_title(bookmark_instance.link)
    return await utils.create_bookmark(session, current_user, bookmark_instance, title)


@api_router.get(
    "docs",
    status_code=status.HTTP_200_OK,
    response_model=Page[BookmarkSchema],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def retrieve_list(
    _: Request,
    current_user: User = Depends(get_current_user),
    tag_filter: list[str] = Query(default=[], alias="tag"),
    sort_key: BookmarksSortKey = Query(default=BookmarksSortKey.BY_ID),
    session: AsyncSession = Depends(get_session),
):
    query = utils.build_query_for_retrieve_list_of_bookmarks(current_user, tag_filter, sort_key)
    return await paginate(session, query)
