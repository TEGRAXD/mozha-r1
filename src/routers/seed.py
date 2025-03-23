from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os

from src.database.db import get_db
from resources.seeder import seed_crud
from src.models.schemas import SuccessResponse
from helpers.error_response import error_response_models

router = APIRouter(prefix="/seed", tags=["Seed"])

@router.get("/",
         response_model=SuccessResponse[dict[str, list[str]]],
         responses=error_response_models())
def seed(db: Session = Depends(get_db)):
    prod_mode = os.getenv("PROD_MODE").lower() == "true"

    if prod_mode:
        raise HTTPException(status_code=403, detail="Forbidden")

    created_perms = seed_crud.seed_permissions(db)
    created_roles = seed_crud.seed_roles(db)
    created_users = seed_crud.seed_users(db)
    return SuccessResponse.success("Database seeded successfully", {
        "permissions": created_perms,
        "roles": created_roles,
        "users": created_users,
    })
