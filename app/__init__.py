from fastapi import FastAPI                  #importing FastAPI class 
from .web.cars.api import router as cars_router
from .web.users.api import router as users_router


app = FastAPI(title="Car Report API")         #fastapi instance called as app is created 


# Include routers

app.include_router(cars_router, prefix="/cars", tags=["Cars"])
app.include_router(users_router, prefix="/users", tags=["Users"])
 # sec stash 

# first stash 
