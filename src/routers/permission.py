from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from typing import Annotated

from src.database.db import get_db
from src.models.schemas import SuccessResponse, Permission, PermissionCreate
from helpers.error_response import error_response_models
from src.resources import permission_crud

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.get("/",
         response_model=SuccessResponse[list[Permission]],
         responses=error_response_models())
def get_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    permissions = permission_crud.get_permissions(db, skip=skip, limit=limit)
    return SuccessResponse.success("Permissions retrieved successfully", permissions)

@router.post("/",
          response_model=Permission,
          responses=error_response_models(),
          status_code=201)
def create_permission(permission: Annotated[PermissionCreate, Form()],
                      db: Session = Depends(get_db)):
    db_permission = permission_crud.create_permission(db, permission)
    return SuccessResponse.success("Permission created successfully", db_permission)
