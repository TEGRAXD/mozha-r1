from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.models.models import Permission, Role, User
from src.models.schemas import PermissionCreate, RoleCreate, UserCreate
from src.helpers.hasher import Hasher

def seed_permissions(db: Session):
    created_perms = []

    permissions = [
        "read_user", "create_user", "update_user", "delete_user",
        "read_role", "create_role", "update_role", "delete_role",
        "read_permission", "create_permission", "update_permission", "delete_permission",
        "read_audit_log", "create_audit_log", "update_audit_log", "delete_audit_log",
    ]

    for permission in permissions:
        exists = db.query(Permission).filter(Permission.name == permission).first()
        if not exists:
            db.add(Permission(name=permission))
            created_perms.append(permission)
        
    db.commit()

    return created_perms

def seed_roles(db: Session):
    created_roles = []

    all_permissions = db.query(Permission).all()

    superadmin = db.query(Role).filter(Role.name == "superadmin").first()
    if not superadmin:
        superadmin = Role(name="superadmin", permissions=all_permissions)
        db.add(superadmin)
        created_roles.append("superadmin")
    
    read_perms = [perm for perm in all_permissions if perm.name.startswith("read_")]
    user = db.query(Role).filter(Role.name == "user").first()
    if not user:
        user = Role(name="user", permissions=read_perms)
        db.add(user)
        created_roles.append("user")
    
    db.commit()

    return created_roles

def seed_users(db: Session):
    created_users = []

    superadmin_role = db.query(Role).filter(Role.name == "superadmin").first()
    user_role = db.query(Role).filter(Role.name == "user").first()

    if not db.query(User).filter(User.username == "superadmin", User.email == "superadmin@mail.com").first():
        superadmin = User(username="superadmin", email="superadmin@mail.com", password=Hasher.hash_password("password"),  roles=[superadmin_role])
        db.add(superadmin)
        created_users.append("superadmin")
    
    if not db.query(User).filter(User.username == "user", User.email == "user@mail.com").first():
        user = User(username="user", email="user@mail.com", password=Hasher.hash_password("password"), roles=[user_role])
        db.add(user)
        created_users.append("user")
    
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

    return created_users
