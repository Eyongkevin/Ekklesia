from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.bot.webhook import router as telegram_router
from app.api import invite, church, user, announcement, status, audience, permission
from app.admin.dashboard import setup_admin
from app.core.exceptions.base import AppException
from app.core.exception_handler import app_exception_handler


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your Reflex frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(telegram_router, prefix="/api/v1/telegram", tags=['telegram'])
app.include_router(invite.router, prefix="/api/v1")
app.include_router(church.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(announcement.router, prefix="/api/v1")
app.include_router(status.router, prefix="/api/v1")
app.include_router(audience.router, prefix="/api/v1")
app.include_router(permission.router, prefix="/api/v1")
setup_admin(app)

app.add_exception_handler(AppException, app_exception_handler)