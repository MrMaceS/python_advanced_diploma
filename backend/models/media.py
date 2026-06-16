from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Media(Base):
    """Картинка/медиа в Twitter"""

    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(500), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)

    tweet = relationship("Tweet", back_populates="media", lazy="select")

    def __repr__(self):
        return f"<Media(id={self.id}, file_path='{self.file_path}')>"
