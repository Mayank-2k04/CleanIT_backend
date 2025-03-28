from sqlalchemy import Column, Integer, String, BigInteger, Index, ForeignKey, func, DateTime, Enum, Boolean
from .databaseconnect import base
from sqlalchemy.orm import relationship

class UserOTP(base):
    __tablename__ = "usersOtp"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    otp = Column(String(6), nullable=True)  # Store the latest OTP
    is_verified = Column(Boolean, default=False)# Mark when OTP is verified
    created_at = Column(DateTime, server_default=func.now())

class Student(base):
    __tablename__="Student"
    email = Column(String(100), primary_key=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    r_id = Column(Integer, ForeignKey("Rooms.r_id"), nullable=False)
    phone_number = Column(BigInteger, unique=False, nullable=False)

    room = relationship("Room", back_populates="students")

    __table_args__ = (Index("idx_hostel_room", "r_id","email"),)  # Index for faster search

class Employee(base):
    __tablename__="Employee"
    c_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hostel_block = Column(String(10), nullable=False)
    phone_number = Column(BigInteger, unique=True, nullable=False)
    available = Column(Boolean, default=True)

    tasks = relationship("TaskAssignment",back_populates="employee")
    __table_args__ = (Index("idx_hostel_block", "hostel_block"),)

class Admin(base):
    __tablename__ = "Admins"
    admin_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hostel_block = Column(String(10), nullable=False)
    phone_number = Column(BigInteger, unique=True, nullable=False)
    __table_args__ = (Index("idx_hostel_block1", "hostel_block"),)

class Room(base):
    __tablename__="Rooms"
    r_id = Column(Integer, primary_key=True, index=True)
    hostel_block = Column(String(10), nullable=False)
    room_number = Column(Integer, nullable=False)

    request = relationship("Request",back_populates="room")
    students = relationship("Student", back_populates="room")

class Request(base):
    __tablename__ = "Requests"
    request_id = Column(Integer, primary_key=True, index=True)
    r_id = Column(Integer, ForeignKey("Rooms.r_id"), nullable=False)
    created_time = Column(DateTime, nullable=False, default=func.now())
    deadline = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    progress = Column(Enum("pending", "in process", "completed", name="task_status"), nullable=False, default="pending")

    room = relationship("Room",back_populates="request")

class TaskAssignment(base):
    __tablename__ = "TaskAssignments"
    assignment_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, nullable=False)  # References Request table
    staff_id = Column(Integer, ForeignKey("Employee.c_id"), nullable=False)
    assigned_time = Column(DateTime, nullable=False, default=func.now())  # Auto-assign current timestamp

    employee = relationship("Employee", back_populates="tasks")

"""
Login route
Access room using student email(connect table students)
Admin can view the available employees in their block by checking availability
Mark task as completed
Request a task

"""
