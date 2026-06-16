from typing import List
from pydantic import BaseModel


class UserCreate(BaseModel):
    """Схема для создания пользователя"""

    name: str
    api_key: str


class UserResponse(BaseModel):
    """Простой ответ о пользователе"""

    id: int
    name: str


class ProfileResponse(BaseModel):
    """Полный профиль пользователя (с followers/following)"""

    id: int
    name: str
    followers: List[dict]
    following: List[dict]


class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FollowResponse(BaseModel):
    result: bool
    user: UserOut
