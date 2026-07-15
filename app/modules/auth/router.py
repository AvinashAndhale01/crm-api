from fastapi import APIRouter, HTTPException, status
from app.dependencies.db import SessionDep
from app.modules.users.schema import CreateUser, LoginUser, UserResponse
from app.modules.auth.schema import Token
from app.modules.auth import service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(user: CreateUser, session: SessionDep):
    try:
        return await service.signup(user, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token, status_code=200)
async def login(user: LoginUser, session: SessionDep):
    try:
        return await service.login(user, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
