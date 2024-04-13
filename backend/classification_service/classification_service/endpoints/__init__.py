from .health_check import api_router as health_check_router
from .qa import api_router as get_answer_api_router

list_of_routes = [
    health_check_router,
    get_answer_api_router,
]

__all__ = [
    "list_of_routes",
]
