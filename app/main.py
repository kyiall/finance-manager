from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .api import users, transactions, subscriber_plans, auth, categories
from .core.utils import CustomException

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(transactions.router, prefix="/api", tags=["transactions"])
app.include_router(subscriber_plans.router, prefix="/api", tags=["subscriber-plans"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(categories.router, prefix="/api", tags=["categories"])


@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"details": exc.name}
    )
