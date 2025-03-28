from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    name: str
    phone_number: int

class Student(User):
    email : str
    r_id: int

class DisplayStudent(Student):
    class Config:
        orm_mode=True

class Request(BaseModel):
    deadline : str

class StudentLogin(BaseModel):
    email: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str

class OTPRequest(BaseModel):
    phone: str

class OTPVerification(BaseModel):
    phone: str
    code: str

class RoomBase(BaseModel):
    hostel_block: str
    room_number: int

    class Config:
        from_attributes: True

class DisplayRequest(BaseModel):
    assigned_time: datetime
    deadline: Optional[datetime]
    progress: str
    room: RoomBase

    class Config:
        from_attributes: True


