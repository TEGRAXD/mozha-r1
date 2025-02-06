from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import models, schemas
from app.resources import user as user_crud
from app.database.db import SessionLocal, engine

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

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip:int = 0, limit:int = 0, db:Session = Depends(get_db)):
    users = user_crud.get_users(db,skip=skip,limit=limit)
    return users
