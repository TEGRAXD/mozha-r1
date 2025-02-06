from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base
import datetime as dt
from datetime import datetime
import uuid

# Association Table
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String(255), ForeignKey("users.id"), nullable=False),
    Column("role_id", String(255), ForeignKey("roles.id"), nullable=False)
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String(255), ForeignKey("roles.id"), nullable=False),
    Column("permission_id", String(255), ForeignKey("permissions.id"), nullable=False)
)

# user_permission = Table(
#     "user_permission",
#     Base.metadata,
#     Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
#     Column("permission_id", Integer, ForeignKey("permissions.id"), nullable=False)
# )

class Role(Base):
    __tablename__ = "roles"

    id = Column(String(255), primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    role_name = Column(String(255), unique=True, index=True, nullable=False)
    role_description = Column(String(255), nullable=True)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String(255), primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    permission_name = Column(String(255), unique=True, index=True, nullable=False)
    permission_details = Column(JSON, nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(dt.timezone.utc), nullable=False)

    audit_logs = relationship("AuditLog", back_populates="user")

# class UserRoles(Base):
#     __tablename__ = "user_roles"

#     user_id = Column(String(255), ForeignKey("users.id"), nullable=False)
#     role_id = Column(String(255), ForeignKey("roles.id"), nullable=False)

# class RolePermissions(Base):
#     __tablename__ = "role_permissions"

#     role_id = Column(String(255), ForeignKey("roles.id"), nullable=False)
#     permission_id = Column(String(255), ForeignKey("permissions.id"), nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(255), primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    action = Column(String(255), nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now(dt.timezone.utc), nullable=False)

    user = relationship("User", back_populates="audit_logs")