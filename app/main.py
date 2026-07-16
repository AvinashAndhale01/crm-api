from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.contacts.router import router as contacts_router
from app.db.session import engine
from app.db.base import Base
from app.db import models


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def status():
    return "Ok"


app.include_router(auth_router)
app.include_router(contacts_router)
