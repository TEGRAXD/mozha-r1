from pydantic import BaseModel
from datetime import datetime
import uuid

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    created_at: datetime

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    role_name: str
    role_description: str | None = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class PermissionBase(BaseModel):
    permission_name: str
    permission_details: dict

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class UserRolesBase(BaseModel):
    pass

class UserRolesCreate(UserRolesBase):
    pass

class UserRoles(UserRolesBase):
    user_id: uuid.UUID
    role_id: uuid.UUID

    class Config:
        orm_mode = True

class RolePermissionsBase(BaseModel):
    pass

class RolePermissionsCreate(RolePermissionsBase):
    pass

class RolePermissions(RolePermissionsBase):
    role_id: uuid.UUID
    permission_id: uuid.UUID

    class Config:
        orm_mode = True

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
        orm_mode = True