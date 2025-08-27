from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.routes.users import router as user_router
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan management для ресурсов"""
    logger.info("Запуск приложения...")
    yield
    logger.info("Остановка приложения...")


app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="API для управления пользователями",
    lifespan=lifespan,
)

ROUTERS = (user_router,)

for r in ROUTERS:
    app.include_router(r)


def main():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
