from .. import schemas,databaseconnect
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from myapi.auth import authorization
from myapi.student import querylogics
from typing import List

router = APIRouter(
    prefix="/student",
    tags=["Student_Protected_routes"]
)


@router.post("/request")
def create_request(
        request: schemas.Request,
        user_detail: dict=Depends(authorization.get_current_student),
        db: Session=Depends(databaseconnect.get_db)
):
    return querylogics.create_request(request, db, user_detail)


@router.get("/request",response_model=schemas.DisplayCurrentRequest)
def get_request(
        user_detail: dict=Depends(authorization.get_current_student),
        db: Session=Depends(databaseconnect.get_db)
):
    return querylogics.get_request(user_detail, db)

@router.get("/details", response_model=schemas.DisplayStudent)
def get_details(
        user_detail: dict=Depends(authorization.get_current_student),
        db: Session=Depends(databaseconnect.get_db)
):
    return querylogics.get_details(user_detail, db)

@router.get("/history", response_model=List[schemas.History])
def history(
        user_detail: dict=Depends(authorization.get_current_student),
        db: Session=Depends(databaseconnect.get_db)
):
    return querylogics.history(user_detail, db)
