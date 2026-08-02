from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.upload import router as upload_router
from app.api.analysis import router as analysis_router
from app.api.reports import router as reports_router
from app.api.chat import router as chat_router
from app.api.garages import router as garages_router
from app.api.mechanics import router as mechanics_router
from app.api.admin import router as admin_router
from app.core.database import engine, Base
from app.core.config import settings
from app.api.auth import router as auth_router
from app.core.database import engine, Base
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(upload_router, prefix=f"{settings.API_V1_STR}/vehicles", tags=["vehicles"])
app.include_router(analysis_router, prefix=f"{settings.API_V1_STR}/inspections", tags=["analysis"])
app.include_router(reports_router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/inspections", tags=["chat"])
app.include_router(garages_router, prefix=f"{settings.API_V1_STR}/garages", tags=["garages"])
app.include_router(mechanics_router, prefix=f"{settings.API_V1_STR}/mechanics", tags=["mechanics"])
app.include_router(admin_router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])

# Mount uploads directory for serving images statically (for development)
import os
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # For dev: drop and create tables (in production use alembic)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to AutoMedi.AI API"}

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "healthy", "service": "AutoMedi.AI"}
