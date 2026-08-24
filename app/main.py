from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, products, delivery, orders
from app.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="TechBox AI-powered electronics store API",
)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(products.router)
app.include_router(delivery.router)
app.include_router(orders.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }