from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.middlewares.auth import api_key_auth
from backend.services.tweet_service import save_media_file

medias_router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
MEDIA_DIR.mkdir(exist_ok=True)


@medias_router.post("/medias", response_model=dict)
async def upload_media_endpoint(
    file: UploadFile = File(...),
    user=Depends(api_key_auth),
):
    """
    Загрузить файл-картинку.

    Endpoint: POST /api/medias
    Headers: api-key: <str>
    Form: file="image.jpg"

    Return:
        { "result": true, "media_id": int }
    """
    session: Session = SessionLocal()

    try:
        filename = file.filename

        if filename is None:
            raise HTTPException(
                status_code=400,
                detail={
                    "result": False,
                    "error_type": "INVALID_FILENAME",
                    "error_message": "Filename is missing",
                },
            )

        file_path = MEDIA_DIR / filename

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        media_id = save_media_file(
            session, tweet_id=None, file_path=f"media/{filename}"
        )

        return {"result": True, "media_id": media_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "UPLOAD_MEDIA_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()
