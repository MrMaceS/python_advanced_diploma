from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models import Follow, Tweet, User


def follow_user(
    session: Session,
    current_user: User,
    target_user_id: int,
) -> User:
    """
    Подписаться (follow) на пользователя.
    """
    if current_user.id == target_user_id:
        raise HTTPException(
            status_code=400,
            detail={
                "result": False,
                "error_type": "CANNOT_FOLLOW_SELF",
                "error_message": "You cannot follow yourself",
            },
        )

    target_user = session.query(User).filter(User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "USER_NOT_FOUND",
                "error_message": f"User {target_user_id} not found",
            },
        )

    existing = (
        session.query(Follow)
        .filter(
            Follow.user_id == current_user.id,
            Follow.following_user_id == target_user_id,
        )
        .first()
    )
    if existing:
        return target_user

    follow = Follow(user_id=current_user.id, following_user_id=target_user_id)
    session.add(follow)
    session.commit()
    session.refresh(target_user)
    return target_user


def unfollow_user(
    session: Session,
    current_user: User,
    target_user_id: int,
) -> User:
    """
    Отписаться от пользователя.
    """
    target_user = session.query(User).filter(User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "USER_NOT_FOUND",
                "error_message": f"User {target_user_id} not found",
            },
        )

    existing = (
        session.query(Follow)
        .filter(
            Follow.user_id == current_user.id,
            Follow.following_user_id == target_user_id,
        )
        .first()
    )
    if existing:
        session.delete(existing)
        session.commit()

    session.refresh(target_user)
    return target_user


def _build_profile_dict(session: Session, user: User) -> Dict:
    """
    Собрать словарь профиля пользователя с followers / following.
    """
    followers = session.query(Follow).filter(Follow.following_user_id == user.id).all()

    followers_list = []
    for f in followers:
        follower_user = session.query(User).filter(User.id == f.user_id).first()
        if follower_user:
            followers_list.append({"id": follower_user.id, "name": follower_user.name})

    following = session.query(Follow).filter(Follow.user_id == user.id).all()

    following_list = []
    for f in following:
        following_user = (
            session.query(User).filter(User.id == f.following_user_id).first()
        )
        if following_user:
            following_list.append(
                {"id": following_user.id, "name": following_user.name}
            )

    return {
        "id": user.id,
        "name": user.name,
        "followers": followers_list,
        "following": following_list,
    }


def get_my_profile(session: Session, current_user: User) -> Dict:
    """
    Профиль текущего пользователя.
    """
    return _build_profile_dict(session, current_user)


def get_profile_by_id(session: Session, user_id: int) -> Dict:
    """
    Профиль произвольного пользователя по ID.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "USER_NOT_FOUND",
                "error_message": f"User {user_id} not found",
            },
        )
    return _build_profile_dict(session, user)


def get_user_tweets(session: Session, user_id: int) -> List[dict]:
    """
    Получить список твитов конкретного пользователя.
    Сортировка: по дате (сначала новые).
    """
    tweets = (
        session.query(Tweet)
        .filter(Tweet.author_id == user_id)
        .order_by(Tweet.created_at.desc())
        .all()
    )

    result = []
    for tweet in tweets:
        attachments = [m.file_path for m in tweet.media]

        likes_list = [
            {"user_id": like.user_id, "name": like.user.name} for like in tweet.likes
        ]

        result.append(
            {
                "id": tweet.id,
                "content": tweet.content,
                "attachments": attachments,
                "author": {
                    "id": tweet.author.id,
                    "name": tweet.author.name,
                },
                "likes": likes_list,
                "created_at": tweet.created_at,
                "likes_count": tweet.likes_count,
            }
        )

    return result
