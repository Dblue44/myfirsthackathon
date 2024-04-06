import io
from typing import Literal

from celery.result import AsyncResult
from fastapi import (
    status,
    APIRouter,
    UploadFile,
    HTTPException
)
from fastapi.responses import (
    JSONResponse,
    StreamingResponse
)

from .tasks import stick_images
from src.core import global_redis
from .service import cast_array_to_bytes, guess_extension

TaskState = Literal["PENDING", "STARTED", "RETRY", "FAILURE", "SUCCESS"]
router = APIRouter(tags=["Sticking images"], prefix="/images")


@router.post("/stick", summary="Sticking 2 images")
async def stick_photos(images: list[UploadFile]) -> JSONResponse:
    if len(images) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only 2 photos allowed"
        )
    image1 = await images[0].read()
    image2 = await images[1].read()
    task_id = stick_images.apply_async(
        kwargs={
            "image1": image1,
            "image2": image2,
            "filename": f"{images[0].filename.split('.')[:-1]}_{images[1].filename}"
        },
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"task_id": task_id})


@router.get("/tasks/{task_id}", summary="Polling task")
def poll_task(task_id: str) -> StreamingResponse:
    task_result = AsyncResult(id=task_id)
    filename = global_redis.get(name=task_id) or ''
    if task_result.state == "FAILURE":
        global_redis.delete(name=task_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task failed"
        )
    if task_result.state == "PENDING":
        return StreamingResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content="Task pending",
            media_type="text/plain"
        )
    if task_result.state in ("STARTED", "RETRY"):
        return StreamingResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content="Task in progress",
            media_type="text/plain"
        )
    global_redis.delete(name=task_id)
    return StreamingResponse(
        status_code=status.HTTP_200_OK,
        content=io.BytesIO(cast_array_to_bytes(
            dst=task_result.result,
            extension=guess_extension(filename=filename))
        ),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
