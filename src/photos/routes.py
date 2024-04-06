from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import APIRouter, UploadFile, HTTPException, status


router = APIRouter(tags=["Sticking photos"], prefix="/files")


@router.post("/stick", summary="Sticking 2 photos")
def stick_photos(files: list[UploadFile]) -> JSONResponse:
    if len(files) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only 2 photos allowed"
        )
    # task_id = ...  # todo apply async celery task for sticking
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"task_id": "test"})


@router.get("/{task_id}", summary="Polling task")
def poll_task(task_id: int) -> StreamingResponse:
    pass
