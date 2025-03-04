from sqlalchemy import Column, Integer, String
from .databaseconnect import base

class User(base):
    s_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hostel_block = Column(String)
    room_number = Column(Integer)
    phone_number = Column(Integer)