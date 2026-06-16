from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TweetCreate(BaseModel):
    """Схема для создания твита (входящий JSON)"""

    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class TweetResponse(BaseModel):
    """Схема ответа при создании твита"""

    result: bool
    tweet_id: int


class TweetWithAuthor(BaseModel):
    """Твит с автором (для ленты)"""

    id: int
    content: str
    attachments: List[str]
    author: dict
    likes: List[dict]
    media_urls: list[str]
    created_at: datetime
    likes_count: int

    class Config:
        from_attributes = True
