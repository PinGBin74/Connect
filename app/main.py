import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import psycopg2
from app.settings import Settings
from app.users.auth.handlers import router as auth_router
from app.posts.handlers import router as posts_router
from app.users.user_profile.handlers import router as user_router
from app.users.subscription.handlers import router as subscription_router
from app.users.users_settings.handlers import router as user_settings_router
from app.render.handlers import router as render_router

from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk

settings = Settings()

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
)

app = FastAPI(
    title="Connect Site API",
    description="API for connect information and user management",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    max_age=3600,
)

try:
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    print("Successfully connected to the database")
except Exception as e:
    print(f"Error connecting to the database: {e}")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


app.include_router(posts_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(subscription_router)
app.include_router(user_settings_router)
app.include_router(render_router)
