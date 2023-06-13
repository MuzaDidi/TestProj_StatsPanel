from databases import Database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.handlers import router
from core import system_config
import uvicorn
from db.db_manager import get_db


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)

    origins = [
        "http://localhost",
        "http://localhost:80",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.on_event('startup')
    async def startup():
        database: Database = get_db()
        await database.connect()

    @application.on_event("shutdown")
    async def shutdown():
        database: Database = get_db()
        await database.disconnect()

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run('main:app', host=system_config.app_host, port=int(system_config.app_port), reload=True)
