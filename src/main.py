from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Annotated
import os
from dotenv import load_dotenv
load_dotenv(override=True)

from src.database.db import engine, get_db
from src.models import models, schemas
from src.resources import user_crud, permission_crud
from resources.seeder import seed_crud
from helpers.error_response import error_response_models
from src.routers import seed, permission, user

prod_mode = os.getenv("PROD_MODE").lower() == "true"

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mozha-R1-API",
    description="API for Mozha-R1",
    version="1.0.0",
)

routers = [
    seed.router,
    permission.router,
    user.router,
]

for router in routers:
    app.include_router(router)

@app.get("/", response_model=schemas.SuccessResponse[dict[str, str]])
async def root():
    return schemas.SuccessResponse.success("Welcome to Mozha-R1 API", {"version": "1.0.0", "created_by": "TEGRAXD"})

@app.exception_handler(404)
async def not_found_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content=schemas.ErrorResponse(
            status="error",
            message="Not found",
            error=[schemas.Error(msg="Resource not found", loc=None)],
        ).model_dump(),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
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
