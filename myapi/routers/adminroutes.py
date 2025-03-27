from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from .. import schemas, databaseconnect, models
from ..auth import authorization
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["Admin Routes"]
)


@router.get("/get_students", status_code=200,response_model=List[schemas.DisplayStudent])
def get_students(db: Session=Depends(databaseconnect.get_db), details:dict = Depends(authorization.get_current_worker)):
    if details['role'] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    records = db.query(models.Student).all()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No records found!")
    return records