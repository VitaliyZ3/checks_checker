from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.auth_core import auth_controller
from src.invoice_core import invoice_controller


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])
    app.include_router(invoice_controller.router, prefix="/invoice", tags=["Invoices"])


def create_app() -> FastAPI:
    app = FastAPI(
        title="Some name",
        description="Soime description",
        docs_url="/docs"
    )
    init_routers(app=app)
    init_cors(app=app)

    return app


app = create_app()
