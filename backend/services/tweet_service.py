from typing import List, Optional, cast
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models import Tweet, Media, Like, Follow, User


def create_tweet(
    session: Session,
    user: User,
    content: str,
    media_ids: Optional[List[int]] = None,
) -> int:
    """
    Создать твит.

    - Валидируем длину текста
    - Создаём Tweet в БД
    - Привязываем медиа (если есть media_ids)

    Returns:
        tweet_id: int
    """
    content = content.strip()

    if not content:
        raise HTTPException(
            status_code=400,
            detail={
                "result": False,
                "error_type": "EMPTY_TWEET",
                "error_message": "Tweet content cannot be empty",
            },
        )

    if len(content) > 1000:
        raise HTTPException(
            status_code=400,
            detail={
                "result": False,
                "error_type": "TWEET_TOO_LONG",
                "error_message": "Tweet content is too long (max 1000 chars)",
            },
        )

    tweet = Tweet(content=content, author_id=user.id)
    session.add(tweet)
    session.flush()

    if media_ids:
        medias = session.query(Media).filter(Media.id.in_(media_ids)).all()
        for media in medias:
            media.tweet_id = tweet.id

    session.commit()
    return cast(int, tweet.id)


def delete_tweet(session: Session, user: User, tweet_id: int) -> dict:
    """
    Удалить твит, если он принадлежит текущему пользователю.
    """
    tweet = session.query(Tweet).filter(Tweet.id == tweet_id).first()

    if not tweet:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "TWEET_NOT_FOUND",
                "error_message": f"Tweet {tweet_id} not found",
            },
        )

    if tweet.author_id != user.id:
        raise HTTPException(
            status_code=403,
            detail={
                "result": False,
                "error_type": "FORBIDDEN",
                "error_message": "You can delete only your own tweets",
            },
        )

    session.query(Like).filter(Like.tweet_id == tweet_id).delete()
    session.query(Media).filter(Media.tweet_id == tweet_id).delete()

    session.delete(tweet)
    session.commit()

    return {"result": True}


def add_like(session: Session, user: User, tweet_id: int) -> None:
    """
    Поставить лайк на твит.
    """
    tweet = session.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "TWEET_NOT_FOUND",
                "error_message": f"Tweet {tweet_id} not found",
            },
        )

    existing = (
        session.query(Like)
        .filter(Like.user_id == user.id, Like.tweet_id == tweet_id)
        .first()
    )

    if existing:
        return

    like = Like(user_id=user.id, tweet_id=tweet_id)
    session.add(like)
    session.commit()


def remove_like(session: Session, user: User, tweet_id: int) -> None:
    """
    Убрать лайк с твита.
    """
    existing = (
        session.query(Like)
        .filter(Like.user_id == user.id, Like.tweet_id == tweet_id)
        .first()
    )
    if not existing:
        return

    session.delete(existing)
    session.commit()


def get_feed(session: Session, user: User) -> List[dict]:
    """
    Получить ленту твитов:
    - от пользователей, которых текущий user фолловит
    - и от самого пользователя (его собственные твиты).
    Сортировка: по количеству лайков (по убыванию), потом по дате (сначала новые).
    """
    following_ids = [
        f.following_user_id
        for f in session.query(Follow).filter(Follow.user_id == user.id).all()
    ]

    source_ids = set(following_ids)
    source_ids.add(user.id)

    if not source_ids:
        return []

    tweets = session.query(Tweet).filter(Tweet.author_id.in_(source_ids)).all()

    tweets_sorted = sorted(
        tweets,
        key=lambda t: (t.likes_count, t.created_at),
        reverse=True,
    )

    result = []
    for tweet in tweets_sorted:
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


def save_media_file(session: Session, tweet_id: Optional[int], file_path: str) -> int:
    """
    Сохранить запись о медиа-файле в БД.

    Используется в:
    - /api/medias (сначала без tweet_id)
    - при создании твита (привязка media_id к tweet_id)
    """
    media = Media(tweet_id=tweet_id, file_path=file_path)
    session.add(media)
    session.commit()
    session.refresh(media)
    return cast(int, media.id)
