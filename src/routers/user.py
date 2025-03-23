from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from src.database.db import get_db
from src.models.models import User as UserModel
from src.models.schemas import SuccessResponse, User, UserCreate
from helpers.error_response import error_response_models
from src.resources import user_crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/",
         response_model=SuccessResponse[list[User]],
         responses=error_response_models())
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return SuccessResponse.success("Users retrieved successfully", users)

@router.post("/",
          response_model=User,
          responses=error_response_models(),
          status_code=201)
def post_user(user: Annotated[UserCreate, Form()], db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user.create_user(db, user)