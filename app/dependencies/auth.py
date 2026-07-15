from typing import Annotated
import jwt
from fastapi import HTTPException, Session, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.modules.users.model import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: Session
):
    creadentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise creadentials_exception
    except jwt.InvalidTokenError:
        raise creadentials_exception
    user = session.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise creadentials_exception
    return user
