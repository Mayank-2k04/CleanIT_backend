from sqlalchemy import Column, Integer, String, BigInteger, Index, ForeignKey, func, DateTime, Enum
from .databaseconnect import base

class Student(base):
    __tablename__="Student"
    email = Column(String(100), primary_key=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    r_id = Column(Integer, ForeignKey("Rooms.r_id"), nullable=False)
    phone_number = Column(BigInteger, unique=True, nullable=False)
    __table_args__ = (Index("idx_hostel_room", "hostel_block", "room_number","email"),)  # Index for faster search

class Employee(base):
    __tablename__="Cleaners"
    c_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hostel_block = Column(String(10), nullable=False)
    phone_number = Column(BigInteger, unique=True, nullable=False)
    __table_args__ = (Index("idx_hostel_block", "hostel_block"),)

class Admin(base):
    __tablename__ = "Admins"
    admin_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hostel_block = Column(String(10), nullable=False)
    phone_number = Column(BigInteger, unique=True, nullable=False)
    __table_args__ = (Index("idx_hostel_block", "hostel_block"),)

class Rooms(base):
    r_id = Column(Integer, primary_key=True, index=True)
    hostel_block = Column(String(10), nullable=False)
    room_number = Column(Integer, nullable=False)

class Request(base):
    __tablename__ = "Requests"
    request_id = Column(Integer, primary_key=True, index=True)
    r_id = Column(Integer, ForeignKey("Rooms.r_id"), nullable=False)
    assigned_time = Column(DateTime, nullable=False, default=func.now())
    completion_time = Column(DateTime, nullable=True)
    status = Column(Enum("pending", "in process", "completed", name="task_status"), nullable=False, default="pending")

class TaskAssignment(base):
    __tablename__ = "TaskAssignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("Requests.request_id"), nullable=False)  # References Request table
    staff_id = Column(Integer, ForeignKey("Staff.staff_id"), nullable=False)  # References Staff table
    assigned_time = Column(DateTime, nullable=False, default=func.now())  # Auto-assign current timestamp
    completion_time = Column(DateTime, nullable=True)  # Will be updated when task is completed



