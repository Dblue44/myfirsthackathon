import io
import logging

from fastapi import (
    status,
    APIRouter,
    UploadFile,
    HTTPException
)
from fastapi.responses import StreamingResponse

from .service import (
    stitch_images,
    cast_array_to_bytes
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Stitching images"], prefix="/images")


@router.post("/stitch", summary="Stitching 2 images")
async def stick_photos(images: list[UploadFile]) -> StreamingResponse:
    if len(images) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only 2 photos allowed"
        )
    image1 = await images[0].read()
    image2 = await images[1].read()
    filename = f"{'.'.join(images[0].filename.split('.')[:-1])}_{images[1].filename}"

    return StreamingResponse(
        status_code=status.HTTP_200_OK,
        content=io.BytesIO(cast_array_to_bytes(
            dst=stitch_images(image1=image1, image2=image2),
            extension=f".{filename.split('.')[-1]}"
        )),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
