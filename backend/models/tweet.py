from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Tweet(Base):
    """Твит — сообщение пользователя"""

    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(1000), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship("User", back_populates="tweets", lazy="select")
    likes = relationship("Like", back_populates="tweet", lazy="select")
    media = relationship("Media", back_populates="tweet", lazy="select")

    @property
    def likes_count(self):
        return len(self.likes)

    def __repr__(self):
        return f"<Tweet(id={self.id}, content='{self.content[:50]}...')>"
