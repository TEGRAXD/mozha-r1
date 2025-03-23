from pydantic import BaseModel, EmailStr
from typing import Generic, Optional, TypeVar, Union
from uuid import UUID
from datetime import datetime

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None

    @classmethod
    def success(cls, message: str, data: Optional[T] = None):
        return cls(status="success", message=message, data=data)

class Error(BaseModel):
    loc: Optional[list[Union[str, int]]]
    msg: str
    type: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str
    message: str
    error: list[Error]


class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: UUID
    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    permission_ids: list[UUID] = []

class Role(RoleBase):
    id: UUID
    permissions: list[Permission]
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role_ids: list[UUID] = []

class User(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    roles: list[Role]
    class Config:
        from_attributes = True

class AuditLogBase(BaseModel):
    action: str

class AuditLogCreate(AuditLogBase):
    user_id: UUID

class AuditLog(AuditLogBase):
    id: UUID
    timestamp: datetime
    class Config:
        from_attributes = True
