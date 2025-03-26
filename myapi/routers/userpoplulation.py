from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, databaseconnect, models
from ..functions import authorization


router = APIRouter(
    # prefix="", use when I ll have multiple routes
    tags=["Database population"]
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(
        request : schemas.Student,
        db : Session=Depends(databaseconnect.get_db),
        email: str = Depends(authorization.get_current_user)):

    admin_user = db.query(models.Student).filter(models.Student.email == email).first()
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to create a user."
        )

    new_user = models.Student(**request.model_dump())
    if not new_user:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail="Record not created!")
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists or invalid data!")