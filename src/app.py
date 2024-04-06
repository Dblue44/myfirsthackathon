from fastapi import FastAPI, Depends

from src.auth import token_auth
from src.config import Config
from src.images.routes import router

config = Config()
app = FastAPI(
    title="Stitching photos",
    dependencies=[Depends(token_auth(token=config.token))],
    root_path="/api/v1"
)

app.include_router(router)
