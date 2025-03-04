from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import schemas, models
from .databaseconnect import engine, local_session

app = FastAPI()
models.base.metadata.create_all(engine)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.User, db : Session=Depends(get_db)):
    new_user = models.User(**request.model_dump())
    if not new_user:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail="Record not created!")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

