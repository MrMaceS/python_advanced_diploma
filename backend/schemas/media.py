from pydantic import BaseModel


class MediaResponse(BaseModel):
    """Ответ при загрузке медиа"""

    result: bool
    media_id: int
