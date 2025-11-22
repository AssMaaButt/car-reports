from fastapi import FastAPI
from .web.cars.api import router as cars_router
from .web.users.api import router as users_router
from .db import init_db

app = FastAPI(title="Car Report API")
init_db()

# Include routers

app.include_router(cars_router, prefix="/cars", tags=["Cars"])
app.include_router(users_router, prefix="/users", tags=["Users"])
