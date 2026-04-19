from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from oa_vibe_api.db.config import TORTOISE_CONFIG
from oa_vibe_api.log import configure_logging
from oa_vibe_api.web.api.router import api_router
from oa_vibe_api.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="oa_vibe_api",
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )

    return app
