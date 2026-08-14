from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import close_client
from app.routers import records

app = FastAPI(
    title="Traditional Fermented Beverages Research API",
    description="Generic CRUD API over MongoDB Atlas collections, one per source dataset file.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://crops-frontend-1oewzq85v-aryans-projects-0f6436b8.vercel.app",
        "http://localhost:5173",  # for local dev with Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.on_event("shutdown")
async def shutdown_event():
    await close_client()
