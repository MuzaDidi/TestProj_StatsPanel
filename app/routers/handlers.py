import logging
from fastapi import APIRouter
from routers import auth_router, users_router, metrics_router


logger = logging.getLogger(__name__)
handler = logging.FileHandler('app.log')
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter()
router.include_router(users_router.router, tags=['User'])
router.include_router(auth_router.router, tags=['Auth'])
router.include_router(metrics_router.router, tags=['Metrics'])


@router.get("/")
def index():
    logger.info("Запрос успешно обработан")
    return {"status_code": 200, "detail": "ok", "result": "working"}