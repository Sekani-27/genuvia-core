import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request, status

from app.capture import process_update
from app.config import TELEGRAM_SECRET
from app.storage import close_pool, init_schema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_schema()
    logger.info("Schema ready")
    yield
    await close_pool()


app = FastAPI(title="Genuvia Core", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook/telegram")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, str]:
    if x_telegram_bot_api_secret_token != TELEGRAM_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    update: dict[str, Any] = await request.json()
    await process_update(update)
    return {"ok": "true"}
