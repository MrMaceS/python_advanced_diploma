from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from backend.database import Base


class Like(Base):
    """Лайк пользователя на твит"""

    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "tweet_id"),)

    user = relationship("User", back_populates="likes", lazy="select")
    tweet = relationship("Tweet", back_populates="likes", lazy="select")

    def __repr__(self):
        return f"<Like(user_id={self.user_id}, tweet_id={self.tweet_id})>"
