from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.providers.database_provider import get_session
from src.providers.password_provider import hash_password
from src.dao.user_dao import UserDAO
from src.models.user_schemas import UserCreate, UserPublic
from src.models.user_model import User
from src.models.auth_schemas import LoginRequest, TokenResponse
from src.providers.jwt_provider import create_access_token
from src.providers.password_provider import hash_password, verify_password
from src.providers.settings_provider import settings


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserPublic, # Even if more keys are present in the output only the ones under UserPublic will be returned
    status_code=status.HTTP_201_CREATED
)
def register(
    user_create: UserCreate,
    session: Annotated[Session, Depends(get_session)],
):
    user_dao = UserDAO(session)

    existing_user = user_dao.get_by_email(user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = User(
        email=user_create.email,
        hashed_password=hash_password(user_create.password)
    )

    created_user = user_dao.create(user)

    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user",
        )
    
    return created_user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_request: LoginRequest,
    session: Annotated[Session, Depends(get_session)],
):
    user_dao = UserDAO(session)
    user = user_dao.get_by_email(login_request.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    password_is_valid = verify_password(
        plain_password=login_request.password,
        hashed_password=user.hashed_password,
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
    