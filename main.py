from fastapi import FastAPI
from app.routes import orders

app = FastAPI()
app.include_router(orders.router)
