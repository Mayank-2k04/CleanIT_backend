from datetime import datetime
from .. import schemas, models
from fastapi import HTTPException,status
from sqlalchemy.orm import Session


def create_request(
        request: schemas.Request,
        db: Session,
        user_detail: dict
                   ):
    student_email = user_detail["id"]
    student = db.query(models.Student).filter(models.Student.email == student_email).first()
    s_r_id = student.r_id

    old_req = db.query(models.Request).filter(
        models.Request.r_id == s_r_id,
        models.Request.progress.in_(["pending", "in process"])
    ).first()

    if old_req:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pending request found!")

        # Convert deadline from string to datetime
    try:
        deadline_datetime = datetime.fromisoformat(request.deadline)  # Expecting an ISO 8601 formatted string
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid deadline format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"
        )

    new_request = models.Request(
        r_id=s_r_id,
        created_time=datetime.now(),
        deadline=deadline_datetime,
        progress="pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {
        "message": "Request created successfully",
        "request_id": new_request.request_id,
        "room_id": s_r_id
    }

def get_request(
        user_detail: dict,
        db: Session
):
    student = db.query(models.Student).filter(
        models.Student.email == user_detail['id']
    ).first()
    room_id = student.r_id
    req = db.query(models.Request).filter(
        models.Request.r_id == room_id,
        models.Request.progress.in_(["pending", "in process"])
    ).first()
    if not req:
        raise HTTPException(status_code=404, detail="No request found for your room.")
    return req

def get_details(
        user_detail: dict,
        db: Session
):
    mail = user_detail['id']
    record = db.query(models.Student).filter(
        models.Student.email == mail
    ).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return record

def history(
        user_detail: dict,
        db: Session
):
    email = user_detail['id']
    student = db.query(models.Student).filter(
        models.Student.email == email
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    room_id = student.r_id
    his = db.query(models.Request).filter(
        models.Request.r_id == room_id,
        models.Request.progress == "completed"
    ).all()

    if not his:
        raise HTTPException(status_code=404, detail="No History Found")
    return his