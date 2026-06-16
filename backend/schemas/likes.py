from pydantic import BaseModel


class LikeResponse(BaseModel):
    """Ответ при лайке/уборке лайка"""

    result: bool
