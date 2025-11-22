# app/web/__init__.py
# This file marks 'web' as a Python package and imports routers.

from fastapi import APIRouter
from app.web.users.api import router as users_router
from app.web.cars.api import router as cars_router

# Main router (optional)
main_router = APIRouter()

@main_router.get("/")
async def home():
    return {"message": "FastAPI app is running successfully!"}
