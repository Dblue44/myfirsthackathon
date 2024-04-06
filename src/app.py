from fastapi import FastAPI, Depends

from src.auth import token_auth
from src.core import global_config
from src.images.routes import router as file_router


app = FastAPI(
    title="Sticking of photos",
    dependencies=[Depends(token_auth(token=global_config.token))],
    root_path="/api/v1"
)

app.include_router(file_router)
