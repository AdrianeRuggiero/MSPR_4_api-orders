from fastapi import FastAPI
from app.routes import orders
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()
Instrumentator().instrument(app).expose(app)
app.include_router(orders.router)
