# services/interfaces.py
from abc import ABC, abstractmethod
from typing import List

from app.models.users import UserCreate, UserInDB, UserResponse


class IUserService(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> UserResponse:
        """Создать нового пользователя"""
        pass

    @abstractmethod
    def get_all_users(self) -> List[UserInDB]:
        """Получение всех пользователей"""
        pass
