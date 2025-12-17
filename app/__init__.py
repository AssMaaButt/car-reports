from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.llm.agent import run_agent  
from app.auth.dependencies import get_current_user
from .web.cars.api import router as cars_router
from .web.users.api import router as users_router

app = FastAPI(title="Car Report API")


app.include_router(cars_router, prefix="/cars", tags=["Cars"])
app.include_router(users_router, prefix="/users", tags=["Users"])


class AgentRequest(BaseModel):
    query: str


@app.post("/agent")
def ask_ai(request: AgentRequest, user_id: int = Depends(get_current_user)):
    """
    Ask the AI agent a question as the logged-in user.
    user_id is automatically extracted from JWT.
    """
    reply = run_agent(request.query, user_id)
    return {"response": reply}
