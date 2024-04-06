from fastapi import APIRouter
from app.core.conf import settings
from app.api.v1.Tests import tests_app

v1 = APIRouter(prefix=settings.API_V1_STR)

v1.include_router(tests_app, prefix='/tests', tags=['Tests'])
