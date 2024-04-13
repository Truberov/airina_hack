from fastapi import FastAPI
from uvicorn import run

from classification_service.config import DefaultSettings, get_settings
from classification_service.endpoints import list_of_routes
from classification_service.utils.common import get_hostname


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Микросервис, реализующий возможность изменять баланс пользователя."

    tags_metadata = [
        {
            "name": "Application Health",
            "description": "API health check.",
        },
        {
            "name": "User Balance Operations",
            "description": "API balance",
        }
    ]

    application = FastAPI(
        title="Balance",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()

if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "balance.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["balance", "tests"],
        log_level="debug",
    )
