from fastapi import FastAPI
from app.bot.webhook import router as telegram_router
from app.api import invite
from app.api import church
from app.api import user
from app.admin.dashboard import setup_admin


app = FastAPI()

app.include_router(telegram_router, prefix="/api/v1/telegram")
app.include_router(invite.router, prefix="/api/v1")
app.include_router(church.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
setup_admin(app)