from fastapi import FastAPI
from . import models
from .databaseconnect import engine
from .routers import studentlogin, userpoplulation, staff_login, adminroutes

app = FastAPI()
models.base.metadata.create_all(engine)

app.include_router(studentlogin.router)
app.include_router(userpoplulation.router)
app.include_router(staff_login.router)
app.include_router(adminroutes.router)


#TODO make schemas for requests


