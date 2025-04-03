from .. import schemas,databaseconnect, models
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends, HTTPException, status
from myapi.auth import authorization
from myapi.staff import querylogics
from typing import List

#Route to get assigned tasks - done and tested
#Route to set task as completed - done and tested

router = APIRouter(
    prefix="/worker",
    tags=["Worker_Protected_routes"]
)

@router.get("/requests",response_model=List[schemas.Tasks])
def get_requests(
        db: Session=Depends(databaseconnect.get_db),
        user_detail: dict=Depends(authorization.get_current_worker)
):
    return querylogics.get_requests(db, user_detail)

@router.put("/request_completed/{req_id}")
def set_complete(
        req_id: int,
        db:Session=Depends(databaseconnect.get_db),
        user_details: dict=Depends(authorization.get_current_worker)
):
    return querylogics.set_complete(db, user_details, req_id)
