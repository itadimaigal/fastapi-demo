from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from ..database import SessionDep
from ..models import Token, User, UserCreate, UserPublic
from ..security import CurrentUser, create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, session: SessionDep):
    if session.exec(select(User).where(User.username == data.username)).first():
        raise HTTPException(status_code=409, detail="Username already taken")
    user = User(username=data.username, hashed_password=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/token", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    query = select(User).where(User.username == form.username)
    user = session.exec(query).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Wrong username or password", headers={"WWW-Authenticate": "Bearer"}
        )
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserPublic)
def me(user: CurrentUser):
    return user
