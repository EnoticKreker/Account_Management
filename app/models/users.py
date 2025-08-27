from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.base import UserBase


class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    balance: Decimal = Field(..., ge=0, description="Баланс пользователя")


class UserCreate(User):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Имя пользователя"
    )
    email: Optional[str] = Field(None, description="Email пользователя")
    balance: Optional[Decimal] = Field(None, ge=0, description="Баланс пользователя")


class UserInDB(User, UserBase):
    """Полная модель пользователя, которая хранится в БД"""

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    """Минимальная модель для ответа при создании"""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "created_at": "2025-08-01T12:00:00",
                    "updated_at": "2025-08-01T12:00:00",
                }
            ]
        }
    )
