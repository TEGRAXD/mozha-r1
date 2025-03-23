from sqlalchemy import Boolean, Column, String, ForeignKey, DateTime, Table
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
from uuid import uuid4, UUID
import datetime as dt
from datetime import datetime
from src.database.db import Base

# Helper UUID
class GUID(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return str(uuid4())
        if isinstance(value, UUID):
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        return UUID(value)

# Association table for many-to-many
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True)
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(dt.timezone.utc), nullable=False)

class Role(Base):
    __tablename__ = "roles"
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)
    name = Column(String(50), unique=True)
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    created_at = Column(DateTime, default=datetime.now(dt.timezone.utc), nullable=False)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)
    name = Column(String(50), unique=True)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    created_at = Column(DateTime, default=datetime.now(dt.timezone.utc), nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"))
    action = Column(String(255))
    timestamp = Column(DateTime, default=datetime.now(dt.timezone.utc), nullable=False)
    user = relationship("User", back_populates="audit_logs")
