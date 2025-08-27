# services/users.py
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.core.settings import app_state
from app.models.users import UserCreate, UserInDB, UserResponse
from app.utils.logger import logger

from .interfaces import IUserService


class UserService(IUserService):
    def _find_user_by_id(self, user_id: UUID) -> UserInDB:
        if user_id is None:
            raise ValueError("ID пользователя не указан")

        data = app_state.users.get(user_id)
        if data is None:
            raise ValueError(f"Пользователь c id = {user_id} не найден")
        return UserInDB(**data)

    def create_user(self, user: UserCreate) -> UserResponse:
        try:
            for existing in app_state.users.values():
                if existing["email"].lower() == user.email.lower():
                    raise ValueError(
                        f"Пользователь с email {user.email} уже существует"
                    )

            now = datetime.utcnow()
            user_id = uuid4()

            new_user = UserInDB(
                id=user_id, created_at=now, updated_at=now, **user.model_dump()
            )

            app_state.users[user_id] = new_user.model_dump()
            app_state.users_list.append(new_user.model_dump())

            return UserResponse(
                id=new_user.id,
                created_at=new_user.created_at,
                updated_at=new_user.updated_at,
            )

        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            error_detail = str(e)
            if "уже существует" in error_detail.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=error_detail
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=error_detail
                )

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    def get_all_users(self) -> List[UserInDB]:
        return app_state.users_list

    def transfer(self, from_user_id: UUID, to_user_id: UUID, amount: Decimal):
        try:
            if from_user_id == to_user_id:
                raise ValueError("Перевод сам себе невозвожен")

            if amount <= 0:
                raise ValueError("Сумма перевода должна быть больше нуля")

            from_user = self._find_user_by_id(from_user_id)
            to_user = self._find_user_by_id(to_user_id)

            if from_user.balance < amount:
                raise ValueError("Недостаточно средств для перевода")

            from_user.balance -= amount
            to_user.balance += amount

            app_state.users[from_user.id] = from_user.model_dump()
            app_state.users[to_user.id] = to_user.model_dump()

            for i, user_in_list in enumerate(app_state.users_list):
                if user_in_list.get("id") == from_user.id:
                    app_state.users_list[i] = from_user.model_dump()
                elif user_in_list.get("id") == to_user.id:
                    app_state.users_list[i] = to_user.model_dump()

            logger.info(
                f"Перевод {amount} от {from_user.email} к {to_user.email} выполнен"
            )

            return {"message": f"Перевод на сумму {amount} доставлен {to_user.name}"}

        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )
