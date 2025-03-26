from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import databaseconnect
from ..functions import login


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("/send-otp", tags=["Login"])
def send_otp(email: str, db : Session=Depends(databaseconnect.get_db)):
    return login.mail_otp(email, db)

@router.post("/verify-otp")
def verify(email: str,otp: str, db: Session=Depends(databaseconnect.get_db)):
    return login.verify_otp(email,otp,db)