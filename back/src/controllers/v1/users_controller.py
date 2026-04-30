from typing import Annotated

from fastapi import APIRouter, Depends

from src.models.user_model import User
from src.models.user_schemas import UserPublic
from src.providers.auth_provider import get_current_active_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserPublic, # Forces the removal of password
)
def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Return current user and just work if token is valid
    """
    return current_user