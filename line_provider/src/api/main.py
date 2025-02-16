from fastapi import FastAPI

from api.exceptions import setup_exception_handlers
from api.lifespan import lifespan
from api.v1.router import api_router as api_router_v1


def web_app_factory():
    app = FastAPI(
        title="line-provider",
        docs_url="/api/docs",
        description="line-provider documentation",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(api_router_v1)
    setup_exception_handlers(app)

    return app
