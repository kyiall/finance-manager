from fastapi import FastAPI

from .api import users, transactions, subscriber_plans, auth

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(transactions.router, prefix="/api", tags=["transactions"])
app.include_router(subscriber_plans.router, prefix="/api", tags=["subscriber-plans"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
