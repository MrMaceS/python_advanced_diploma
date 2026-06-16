from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from backend.database import Base


class Follow(Base):
    """Подписка пользователя на другого пользователя"""

    __tablename__ = "follows"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "following_user_id"),)

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="following",
        lazy="select",
    )

    following_user = relationship(
        "User",
        foreign_keys=[following_user_id],
        back_populates="followers",
        lazy="select",
        overlaps="following,user",
    )

    def __repr__(self) -> str:
        return (
            f"<Follow(user_id={self.user_id}, "
            f"following_user_id={self.following_user_id})>"
        )
