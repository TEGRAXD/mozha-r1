from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Annotated
import os

from src.models import models, schemas
from src.resources import user as user_crud
from src.database.db import SessionLocal, engine

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

@app.get("/", response_model=schemas.SuccessResponse[dict[str, str]])
async def root():
    return schemas.SuccessResponse.success("Welcome to Mozha-R1 API", {"version": "1.0.0", "created_by": "TEGRAXD"})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content=schemas.ErrorResponse(
            status="error",
            message="Validation failed",
            error=exc.errors(),
        ).model_dump(),
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=schemas.ErrorResponse(
            status="error",
            message=exc.detail if isinstance(exc.detail, str) else "HTTP Exception",
            error=[schemas.Error(msg=exc.detail, loc=None)],
        ).model_dump(),
    )

@app.exception_handler(Exception)
async def exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=schemas.ErrorResponse(
            status="error",
            message="Internal Server Error",
            error=[schemas.Error(msg=str(exc), loc=None)],
        ).model_dump(),
    )

@app.get("/users/",
         response_model=schemas.SuccessResponse[list[schemas.User]],
         responses={
             400: {"model": schemas.ErrorResponse},
             422: {"model": schemas.ErrorResponse},
             500: {"model": schemas.ErrorResponse},
             },
        )
def get_users(skip:int = 0, limit:int = 0, db:Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return schemas.SuccessResponse.success("Users retrieved successfully", users)

@app.post("/users/", response_model=schemas.User, status_code=201)
def post_user(user: Annotated[schemas.UserCreate, Form()], db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user)