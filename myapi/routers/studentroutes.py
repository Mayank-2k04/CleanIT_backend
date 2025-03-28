#TODO add route to create a request
from .. import schemas,databaseconnect
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from myapi.auth import authorization
from myapi.student import querylogics

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


@router.get("/request",response_model=schemas.DisplayRequest)
def get_request(
        user_detail: dict=Depends(authorization.get_current_student),
        db: Session=Depends(databaseconnect.get_db)
):
    return querylogics.get_request(user_detail, db)


#TODO add route to view previous requests history
