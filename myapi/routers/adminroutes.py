from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from .. import schemas, databaseconnect, models
from ..auth import authorization
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["Admin Routes"]
)

#show free workers
#show pending tasks
#assign task to a free worker


@router.get("/get_students", status_code=200,response_model=List[schemas.DisplayStudent])
def get_students(db: Session=Depends(databaseconnect.get_db), details:dict = Depends(authorization.get_current_worker)):
    if details['role'] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    records = db.query(models.Student).all()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No records found!")
    return records


@router.get('/unassigned_tasks', status_code=200,response_model=List[schemas.RequestAdminView])
def get_tasks(
        db: Session=Depends(databaseconnect.get_db),
        details: dict=Depends(authorization.get_current_worker)
):
    if details['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    tasks = db.query(models.Request).filter(
        models.Request.progress == "pending"
    ).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks pending.")
    return tasks

@router.get('/free_workers', status_code=200,response_model=List[schemas.WorkerAdminView])
def get_worker(
        db: Session=Depends(databaseconnect.get_db),
        details: dict=Depends(authorization.get_current_worker)
):
    if details['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    worker = db.query(models.Employee).filter(
        models.Employee.available == "True"
    ).all()
    if not worker:
        raise HTTPException(status_code=404, detail="No Worker Free.")
    return worker

@router.post("/assign_task")
def assign_task(
        db: Session=Depends(databaseconnect.get_db),
        details: dict=Depends(authorization.get_current_worker)
):
    pass