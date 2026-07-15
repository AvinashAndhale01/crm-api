from pydantic import BaseModel, ConfigDict

from app.core.enums import RoleType


class UserBase(BaseModel):
    email: str
    password: str


class CreateUser(UserBase):
    full_name: str
    role: RoleType


class LoginUser(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: RoleType
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
