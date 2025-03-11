from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import uvicorn

from xxx import models, schemas
from resources import user as user_crud
from database.db import SessionLocal, engine
from helpers.error_response import custom_error_response

import traceback
from typing import Annotated
import os

prod_mode = os.getenv("PROD_MODE").lower() == "true"

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mozha-R1-API",
    description="API for Mozha-R1",
    version="1.0.0",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error = {
        "path": request.url.path,
    }

    if not prod_mode:
        error["stacktrace"] = list(filter(None, traceback.format_exc().split("\n")))
    
    return custom_error_response(
        status_code=exc.status_code,
        status="error",
        message=exc.detail,
        error=error,
    )

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    error = {
        "path": request.url.path,
    }

    if not prod_mode:
        error["stacktrace"] = list(filter(None, traceback.format_exc().split("\n")))
    
    return custom_error_response(
        status_code=500,
        status="error",
        message="Internal Server Error",
        error=error,
    )

@app.get("/users/", response_model=schemas.ResponseBase[list[schemas.User]])
def get_users(skip:int = 0, limit:int = 0, db:Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return schemas.ResponseBase.success(message="Users succesfully retrieved", data=users)

@app.post("/users/", response_model=schemas.User, status_code=201)
def post_user(user: Annotated[schemas.UserCreate, Form()], db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user)