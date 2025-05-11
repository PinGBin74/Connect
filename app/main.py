from fastapi import FastAPI
from app.settings import Settings
from app.users.auth.handlers import router as auth_router
from app.posts.handlers import router as posts_router
from app.users.user_profile.handlers import router as user_router

from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk

settings = Settings()

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
)

app = FastAPI(
    title="Weather Site API",
    description="API for weather information and user management",
    version="0.1.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts_router)
app.include_router(user_router)
app.include_router(auth_router)
