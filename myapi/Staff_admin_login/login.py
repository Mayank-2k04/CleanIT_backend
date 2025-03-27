

from sqlalchemy.orm import Session
from twilio.rest import Client
import os
from ..schemas import OTPRequest, OTPVerification
from .. import models
from fastapi import HTTPException
from datetime import timedelta
from myapi.config import ACCESS_TIME
from myapi.auth import token

# OTP Module same for admin and worker

account_sid = os.getenv("T_SID") #twilio id
auth_token = os.getenv("T_TOKEN")
client = Client(account_sid, auth_token)

def send_otp(request: OTPRequest, db: Session):
    format_number = "+91" + request.phone
    try:
        verification = client.verify.v2.services("VA8d02e94032d5aca6cb3ebafe60b1ed63") \
            .verifications.create(to=format_number, channel="sms")

        return {"message": "OTP sent successfully", "status": verification.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def verify_otp(request: OTPVerification, db: Session):
    admin_user = db.query(models.Admin).filter(models.Admin.phone_number == request.phone).first()
    worker = db.query(models.Employee).filter(models.Employee.phone_number == request.phone).first()
    if admin_user:
        role="admin"
    elif worker:
        role="worker"
    else:
        raise HTTPException(status_code=400, detail=f"User with phone number {request.phone} not found!")
    try:
        format_phone = "+91" + request.phone
        verification_check = client.verify.v2.services("VA8d02e94032d5aca6cb3ebafe60b1ed63") \
            .verification_checks.create(to=format_phone, code=request.code)

        if verification_check.status == "approved":
            the_token = token.create_token(
                {"sub": request.phone, "role":role},  # verification is done through email for student
                timedelta(minutes=ACCESS_TIME)
            )
            return {"access_token": the_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP")

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Error verifying OTP. Please try again later.")

