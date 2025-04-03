from fastapi import HTTPException, status
from .. import models
from sqlalchemy.orm import Session





def get(db: Session, details: dict):
    if details['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    tasks = db.query(models.Request).filter(
        models.Request.progress == "pending"
    ).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks pending.")
    return tasks

def worker(db: Session, details: dict):
    if details['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    worker = db.query(models.Employee).filter(
        models.Employee.available == "True"
    ).all()
    if not worker:
        raise HTTPException(status_code=404, detail="No Worker Free.")
    return worker