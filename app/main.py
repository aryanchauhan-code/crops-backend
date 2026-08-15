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
    allow_origins=settings.cors_origin_list,
    # Every Vercel deploy of this project gets a new random-hash preview URL
    # (crops-frontend-<hash>-aryans-projects-0f6436b8.vercel.app) -- an exact
    # allow_origins entry goes stale on the next deploy, so match the whole
    # project instead of one deployment's URL. Also covers the two stable
    # aliases that never change (crops-frontend-aryans-projects-....vercel.app
    # and the short crops-frontend.vercel.app).
    allow_origin_regex=r"https://crops-frontend(-[\w-]+)?-aryans-projects-0f6436b8\.vercel\.app|https://crops-frontend\.vercel\.app",
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
