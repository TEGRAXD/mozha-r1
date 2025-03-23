from sqlalchemy.orm import Session
from src.models.models import Permission
from src.models import schemas

def get_permissions(db: Session, skip: int=0, limit: int=100):
    return db.query(Permission).offset(skip).limit(limit).all()

def create_permission(db: Session, permission: schemas.PermissionCreate):
    db_permission = Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission
