from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.models.users import UserCreate, UserInDB, UserResponse
from app.services.users.interfaces import IUserService
from app.services.users.users import UserService
from app.utils.logger import logger

router = APIRouter(prefix="/user/v1", tags=["user"])


def get_user_service() -> IUserService:
    return UserService()


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
)
async def create_user(
    user: UserCreate, user_service: IUserService = Depends(get_user_service)
):
    response = user_service.create_user(user)
    logger.info(f"Пользователь создан: {user.email}")
    return response


@router.get(
    "/users",
    response_model=List[UserInDB],
    status_code=status.HTTP_201_CREATED,
    summary="Возвращает всех пользователей",
)
async def get_all_users(user_service: IUserService = Depends(get_user_service)):
    return user_service.get_all_users()


@router.post("/transfer")
async def transfer_money(
    from_user_id: UUID,
    to_user_id: UUID,
    amount: Decimal,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.transfer(from_user_id, to_user_id, amount)
