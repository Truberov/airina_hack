from balance.endpoints.ping import api_router as application_health_router
from .balance import api_router as balance_router

list_of_routes = [
    application_health_router,
    balance_router,
]

__all__ = [
    "list_of_routes",
]
