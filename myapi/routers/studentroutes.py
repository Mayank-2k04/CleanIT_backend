#TODO add route to create a request
from .. import schemas,databaseconnect
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from myapi.auth import authorization
from myapi.student import querylogics

router = APIRouter(
    prefix="/student"
)

@router.post("/request")
def create_request(
        request: schemas.Request,
        user_detail: dict=Depends(authorization.get_current_student),
        db: Session=Depends(databaseconnect.get_db)
):
    return querylogics.create_request(request, db, user_detail)


#TODO add route to view current request

#TODO add route to view previous requests history
