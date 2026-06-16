from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.middlewares.auth import api_key_auth
from backend.schemas.tweet import TweetCreate
from backend.models.user import User
from backend.services.tweet_service import (
    create_tweet,
    delete_tweet,
    add_like,
    remove_like,
    get_feed,
)

tweets_router = APIRouter()


@tweets_router.post("/tweets", response_model=dict)
def create_tweet_endpoint(
    tweet_data: TweetCreate,
    request: Request,
    user: User = Depends(api_key_auth),
):
    """
    Создать новый твит.

    Endpoint: POST /api/tweets
    Args:
        tweet_data: {tweet_data: str, tweet_media_ids: Optional[List[int]]}
        user: авторизованный пользователь (из middleware)

    Returns:
        {result: true, tweet_id: int}
    """
    session: Session = SessionLocal()

    try:
        tweet_id = create_tweet(
            session, user, tweet_data.tweet_data, tweet_data.tweet_media_ids
        )

        return {"result": True, "tweet_id": tweet_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "CREATE_TWEET_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@tweets_router.delete("/tweets/{tweet_id}", response_model=dict)
def delete_tweet_endpoint(
    tweet_id: int,
    request: Request,
    user: User = Depends(api_key_auth),
):
    """
    Удалить твит (только свой).

    Endpoint: DELETE /api/tweets/
    Args:
        tweet_id: ID твита
        user: авторизованный пользователь

    Returns:
        {result: true}
    """
    session: Session = SessionLocal()

    try:
        return delete_tweet(session, user, tweet_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "DELETE_TWEET_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@tweets_router.post("/tweets/{tweet_id}/likes", response_model=dict)
def add_like_endpoint(
    tweet_id: int,
    request: Request,
    user: User = Depends(api_key_auth),
):
    """
    Лайкнуть твит.

    Endpoint: POST /api/tweets/{id}/likes
    """
    session: Session = SessionLocal()

    try:
        add_like(session, user, tweet_id)
        return {"result": True}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "ADD_LIKE_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@tweets_router.delete("/tweets/{tweet_id}/likes", response_model=dict)
def remove_like_endpoint(
    tweet_id: int,
    request: Request,
    user: User = Depends(api_key_auth),
):
    """
    Убрать лайк с твита.

    Endpoint: DELETE /api/tweets/{id}/likes
    """
    session: Session = SessionLocal()

    try:
        remove_like(session, user, tweet_id)
        return {"result": True}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "REMOVE_LIKE_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@tweets_router.get("/tweets", response_model=dict)
def get_feed_endpoint(
    request: Request,
    user: User = Depends(api_key_auth),
):
    """
    Получить ленту твитов от подписанных пользователей.

    Endpoint: GET /api/tweets
    Returns:
        {result: true, tweets: [...]}
    """
    session: Session = SessionLocal()

    try:
        tweets = get_feed(session, user)
        return {"result": True, "tweets": tweets}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "GET_FEED_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()
