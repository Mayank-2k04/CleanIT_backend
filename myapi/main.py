from fastapi import FastAPI
from . import models
from .databaseconnect import engine
from .routers import login, userpoplulation

app = FastAPI()
models.base.metadata.create_all(engine)

app.include_router(login.router)
app.include_router(userpoplulation.router)





