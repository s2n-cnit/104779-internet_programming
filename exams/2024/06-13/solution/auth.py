from datetime import datetime, timedelta, timezone
from typing import Annotated, List

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model import Token, User, engine
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlmodel import Session

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "hdhfh5jdnb7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

refresh_tokens = []

ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_MINUTES = 120


def get_user(username: str):
    with Session(engine) as session:
        return session.get(User, username)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.DecodeError:
        raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def validate_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        if token in refresh_tokens:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            role: str = payload.get("role")
            if username is None or role is None:
                raise credentials_exception
        else:
            raise credentials_exception
    except (jwt.DecodeError, ValidationError):
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user, token


class RoleChecker:
    def __init__(
        self: "RoleChecker", allowed_role_ids: List[str]
    ) -> "RoleChecker":
        self.allowed_role_ids = allowed_role_ids

    def __call__(
        self: "RoleChecker",
        user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        if user.role_id in self.allowed_role_ids:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions",
        )


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(
        data={"sub": user.id, "role": user.role_id},
        expires_delta=access_token_expires,
    )
    refresh_token = create_token(
        data={"sub": user.id, "role": user.role_id},
        expires_delta=refresh_token_expires,
    )
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
async def refresh_access_token(
    token_data: Annotated[tuple[User, str], Depends(validate_refresh_token)]
):
    user, token = token_data
    access_token = create_token(
        data={"sub": user.id, "role": user.role_id},
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    refresh_token = create_token(
        data={"sub": user.id, "role": user.role_di},
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    refresh_tokens.remove(token)
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)
