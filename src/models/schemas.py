from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Generic, Optional, TypeVar, Union
import uuid

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

class UserBase(BaseModel):
    username: str
    email: EmailStr
    # password: str
    # is_active: bool
    # created_at: datetime

class UserCreate(UserBase):
    # username: str
    # email: EmailStr
    password: str
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = datetime.now()
    # pass

class User(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    role_name: str
    role_description: str | None = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class PermissionBase(BaseModel):
    permission_name: str
    permission_details: dict

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class UserRolesBase(BaseModel):
    pass

class UserRolesCreate(UserRolesBase):
    pass

class UserRoles(UserRolesBase):
    user_id: uuid.UUID
    role_id: uuid.UUID

    class Config:
        from_attributes = True

class RolePermissionsBase(BaseModel):
    pass

class RolePermissionsCreate(RolePermissionsBase):
    pass

class RolePermissions(RolePermissionsBase):
    role_id: uuid.UUID
    permission_id: uuid.UUID

    class Config:
        from_attributes = True

class AuditLogBase(BaseModel):
    user_id: uuid.UUID
    action: str
    details: dict
    created_at: datetime

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: uuid.UUID

    class Config:
        from_attributes = True