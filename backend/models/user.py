from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from backend.database import Base


class User(Base):
    """Пользователь Twitter"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    api_key = Column(String(100), nullable=False, unique=True)

    tweets = relationship("Tweet", back_populates="author", lazy="select")
    likes = relationship("Like", back_populates="user", lazy="select")
    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_user_id",
        back_populates="following_user",
        lazy="select",
    )
    following = relationship(
        "Follow", foreign_keys="Follow.user_id", back_populates="user", lazy="select"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"
