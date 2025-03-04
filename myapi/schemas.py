from pydantic import BaseModel

class User(BaseModel):
    first_name : str
    last_name : str
    hostel_block : str
    room_number : int
    phone_number : int