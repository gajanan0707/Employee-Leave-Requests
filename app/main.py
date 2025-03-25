from fastapi import FastAPI
from .database import engine
from . import models
from .routes import router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Leave Request API")

# Include routers
app.include_router(router)