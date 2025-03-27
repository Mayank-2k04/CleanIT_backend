from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import databaseconnect,schemas
from myapi.Staff_admin_login import login

router = APIRouter(
    prefix="/staff/login",
    tags=["Staff Login"]
)

@router.post("/send-otp")
def send_otp(request: schemas.OTPRequest, db : Session=Depends(databaseconnect.get_db)):
    return login.send_otp(request,db)

@router.post("/verify-otp",response_model=schemas.Token)
def verify(request: schemas.OTPVerification,db: Session=Depends(databaseconnect.get_db)):
    return login.verify_otp(request,db)
