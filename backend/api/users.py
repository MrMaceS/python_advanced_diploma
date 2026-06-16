from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend.schemas.user import FollowResponse
from backend.database import SessionLocal
from backend.middlewares.auth import api_key_auth
from backend.models.user import User
from backend.services.user_service import (
    follow_user,
    unfollow_user,
    get_my_profile,
    get_profile_by_id,
    get_user_tweets,
)

users_router = APIRouter()


@users_router.post("/users/{user_id}/follow", response_model=FollowResponse)
def follow_user_endpoint(
    user_id: int,
    current_user: User = Depends(api_key_auth),
):
    """
    Зафолловить пользователя.
    Введите user_id - кто подписывается
    Ведите api-key - на кого подписывается
    Endpoint: POST /api/users/{user_id}/follow
    """
    session: Session = SessionLocal()
    try:
        target_user = follow_user(session, current_user, user_id)
        return {"result": True, "user": target_user}
    except HTTPException as e:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "FOLLOW_USER_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@users_router.delete("/users/{user_id}/follow", response_model=FollowResponse)
def unfollow_user_endpoint(
    user_id: int,
    current_user: User = Depends(api_key_auth),
):
    """
    Отписаться от пользователя.
    Введите user_id - кто отписывается
    Ведите api-key - от кого отписывается
    Endpoint: DELETE /api/users/{user_id}/follow
    """
    session: Session = SessionLocal()
    try:
        target_user = unfollow_user(session, current_user, user_id)
        return {"result": True, "user": target_user}
    except HTTPException as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "UNFOLLOW_USER_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@users_router.get("/users/me", response_model=dict)
def get_my_profile_endpoint(current_user: User = Depends(api_key_auth)):
    """
    Получить профиль текущего пользователя.

    Endpoint: GET /api/users/me
    """
    session: Session = SessionLocal()
    try:
        profile = get_my_profile(session, current_user)
        return {"result": True, "user": profile}
    except HTTPException as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "GET_MY_PROFILE_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@users_router.get("/users/{user_id}", response_model=dict)
def get_profile_by_id_endpoint(
    user_id: int,
    current_user: User = Depends(api_key_auth),
) -> dict:
    """
    Получить профиль произвольного пользователя по ID.

    Endpoint: GET /api/users/{user_id}
    """
    session: Session = SessionLocal()
    try:
        profile = get_profile_by_id(session, user_id)
        return {"result": True, "user": profile}
    except HTTPException as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "GET_PROFILE_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()


@users_router.get("/users/{user_id}/tweets", response_model=dict)
def get_user_tweets_endpoint(
    user_id: int,
    request: Request,
    user: User = Depends(api_key_auth),
) -> dict:
    """
    Получить список твитов конкретного пользователя.

    Endpoint: GET /api/users/{user_id}/tweets
    Returns:
        {result: true, tweets: [...]}
    """
    session: Session = SessionLocal()

    try:
        tweets = get_user_tweets(session, user_id)
        return {"result": True, "tweets": tweets}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "result": False,
                "error_type": "GET_USER_TWEETS_ERROR",
                "error_message": str(e),
            },
        )
    finally:
        session.close()
