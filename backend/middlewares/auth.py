from fastapi import Header, HTTPException
from backend.database import SessionLocal
from backend.models.user import User


def api_key_auth(api_key: str = Header(..., alias="api-key")) -> User:
    """
    Авторизация через api-key в заголовке

    Args:
        api_key: значение заголовка api-key

    Returns:
        User: найденный пользователь

    Raises:
        HTTPException(401): если api-key нет или пользователь не найден
    """
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.api_key == api_key).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail={
                    "result": False,
                    "error_type": "INVALID_API_KEY",
                    "error_message": f"User with api-key '{api_key}' not found",
                },
            )

        return user

    finally:
        session.close()
