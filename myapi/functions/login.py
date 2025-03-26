from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models,sendemail
from ..config import SECRET_KEY,ALGORITHM,ACCESS_TIME
from datetime import datetime, timedelta, timezone
from jose import jwt


def create_token(data: dict, expiry: timedelta):
    encode_data = data.copy()
    expire = datetime.now(timezone.utc) + expiry
    encode_data.update({"exp":expire})
    return jwt.encode(encode_data, SECRET_KEY, ALGORITHM)


def mail_otp(email: str, db:Session):
    useremail = db.query(models.Student).filter(models.Student.email == email).first()

    if not useremail:
        raise HTTPException(status_code=404, detail="User not found!")

    OTP = sendemail.generate_otp()
    addotp = models.UserOTP(email=useremail.email, otp=OTP)
    db.add(addotp)
    db.commit()
    db.refresh(addotp)
    sendemail.send_otp_email(email, OTP)
    return f"OTP Send to email address {email}. Check spam if not received."


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
    the_token = create_token(
        {"sub": user.email},
        timedelta(minutes=ACCESS_TIME)
    )
    record.delete(synchronize_session=False)
    db.commit()
    return {"access_token": the_token, "token_type": "bearer"}

