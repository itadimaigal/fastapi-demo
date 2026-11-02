from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import create_db_and_tables
from .routers import auth, expenses


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # runs once at startup
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Working example from the itadimaigal FastAPI course.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "version": app.version}
