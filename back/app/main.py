from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Krisha.kz Parser API", version="1.0.0")

# CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import parser, locations, maps

app.include_router(parser.router, prefix="/api/parser", tags=["parser"])
app.include_router(locations.router, prefix="/api/locations", tags=["locations"])
app.include_router(maps.router, prefix="/api/maps", tags=["maps"])

# Инициализация бота при старте приложения (опционально, для вебхуков)
bot_application = None

@app.on_event("startup")
async def startup_event():
    """Инициализация при старте приложения"""
    global bot_application
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        try:
            from app.bot.bot import get_bot_application
            bot_application = get_bot_application()
            await bot_application.initialize()
            await bot_application.start()
            logging.info("Telegram бот инициализирован")
        except Exception as e:
            logging.error(f"Ошибка инициализации бота: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Остановка при завершении приложения"""
    global bot_application
    if bot_application:
        try:
            await bot_application.stop()
            await bot_application.shutdown()
            logging.info("Telegram бот остановлен")
        except Exception as e:
            logging.error(f"Ошибка остановки бота: {e}")

@app.post("/api/bot/webhook")
async def webhook(request: Request):
    """Webhook endpoint для Telegram бота"""
    global bot_application
    if not bot_application:
        return JSONResponse({"error": "Bot not initialized"}, status_code=500)
    
    try:
        from telegram import Update
        data = await request.json()
        update = Update.de_json(data, bot_application.bot)
        await bot_application.process_update(update)
        return JSONResponse({"ok": True})
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/bot/set-webhook")
async def set_webhook(webhook_url: str):
    """Установка webhook URL для бота"""
    global bot_application
    if not bot_application:
        return JSONResponse({"error": "Bot not initialized"}, status_code=500)
    
    try:
        await bot_application.bot.set_webhook(webhook_url)
        return JSONResponse({"ok": True, "webhook_url": webhook_url})
    except Exception as e:
        logging.error(f"Set webhook error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
async def root():
    return {"message": "Krisha.kz Parser API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
