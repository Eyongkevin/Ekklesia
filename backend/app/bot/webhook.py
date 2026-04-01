from fastapi import APIRouter, Request

from app.bot.router import route_update

router = APIRouter()


@router.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()

    route_update(update)

    return {"ok": True}