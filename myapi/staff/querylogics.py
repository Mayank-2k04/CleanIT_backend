from .. import models
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import func


def get_requests(
        db: Session,
        user_detail: dict
):
    if user_detail['role'] != "worker":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized!!")

    worker = db.query(models.Employee).filter(
        models.Employee.phone_number == user_detail['id']
    ).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found!")

    tasks = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.staff_id == worker.c_id
    ).all()

    if not tasks:
        raise HTTPException(status_code=404, detail="Not tasks Assigned!")
    return tasks

def set_complete(
        db: Session,
        user_detail: dict,
        req_id: int
):
    if user_detail['role'] != "worker":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized!!")

    worker = db.query(models.Employee).filter(
        models.Employee.phone_number == user_detail['id']
    ).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found!")

    task = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.request_id == req_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    request = db.query(models.Request).filter(
        models.Request.request_id == req_id
    ).first()

    if request:
        print("found")
        request.progress = "completed"
        request.completed_at = func.now()
        db.add(request)
        db.commit()
        db.refresh(request)

    db.delete(task)
    db.commit()

    return {"message": "Task marked as complete and removed from assignments"}

