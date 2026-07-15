from datetime import timedelta
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.modules.users.model import User
from app.modules.users.schema import CreateUser, LoginUser
from app.modules.auth.schema import Token
from app.core.config import settings


password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")


def authenticate_user(session: Session, username: str, password: str):
    user = session.query(User).filter(User.email == username).first()
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def signup(user: CreateUser, session: Session):
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    hashed_password = get_password_hash(user.password)

    db_user = User(
        **user.model_dump(exclude={"password"}), hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


async def login(user: LoginUser, session: Session):
    db_user = authenticate_user(session, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expire = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expire
    )
    return Token(access_token=access_token, token_type="bearer")
