from fastapi import FastAPI

from database import Base, engine
from models.user_model import User
from routes.user_routes import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "API working"}