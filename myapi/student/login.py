from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models,sendemail
from ..config import ACCESS_TIME
from datetime import datetime, timedelta, timezone
from myapi.auth import token

"""Otp module using email."""


def mail_otp(email: str, db:Session):
    useremail = db.query(models.Student).filter(models.Student.email == email).first()

    if not useremail:
        raise HTTPException(status_code=404, detail="User not found!")

    OTP = sendemail.generate_otp()

    if sendemail.send_otp_email(email, OTP):
        oldotp = db.query(models.UserOTP).filter(models.UserOTP.email == email).first()
        if not oldotp:
            addotp = models.UserOTP(email=useremail.email, otp=OTP)
            db.add(addotp)
            db.commit()
            db.refresh(addotp)
        else:
            oldotp.otp = OTP
            db.commit()
        return f"OTP Send to email address {email}. Check spam if not received."
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Email not sent.")


def verify_otp(email:str, otp:str, db:Session):
    record = db.query(models.UserOTP).filter(models.UserOTP.email == email)
    user = record.first()
    if not user or otp != user.otp:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if user.created_at.tzinfo is None:
        created_at_utc = user.created_at.replace(tzinfo=timezone.utc)
    else:
        created_at_utc = user.created_at

    otp_age = (datetime.now(timezone.utc) - created_at_utc).total_seconds()
    if otp_age > 60 * ACCESS_TIME:
        record.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired!")
    the_token = token.create_token(
        {"sub": user.email, "role":"student"}, #verification is done through email for student
        timedelta(minutes=ACCESS_TIME)
    )
    record.delete(synchronize_session=False)
    db.commit()
    return {"access_token": the_token, "token_type": "bearer"}
