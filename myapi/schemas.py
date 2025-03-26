from pydantic import BaseModel


class User(BaseModel):
    name: str
    phone_number: int

class Student(User):
    email : str
    r_id: int

class Request(BaseModel):
    hostel_block : str
    room_number : str
    scheduled_time : str
    completion_time : str

class StudentLogin(BaseModel):
    email: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str
