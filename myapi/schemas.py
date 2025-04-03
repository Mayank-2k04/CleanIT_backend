from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List


class User(BaseModel):
    name: str
    phone_number: int

class Student(User):
    email : str
    r_id: int

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

class DisplayCurrentRequest(BaseModel):
    created_time: datetime
    deadline: Optional[datetime]
    progress: str
    room: RoomBase

    class Config:
        from_attributes: True

class DisplayStudent(BaseModel):
    name: str
    email: str
    phone_number: int
    room: RoomBase
    class Config:
        from_attributes = True

class History(BaseModel):
    completed_at: datetime
    class Config:
        from_attributes=True

class RequestDeadline(BaseModel):
    deadline: datetime
    class Config:
        from_attributes=True

class Tasks(BaseModel):
    assignment_id: int
    request_id: int
    assigned_time: datetime
    request: RequestDeadline

    class Config:
        from_attributes = True

class RequestAdminView(BaseModel):
    room: RoomBase
    deadline: datetime
    class Config:
        from_attributes = True

class WorkerAdminView(BaseModel):
    c_id: int
    name: str
    hostel_block: str
    class Config:
        from_attributes = True
