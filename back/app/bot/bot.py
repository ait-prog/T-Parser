"""Инициализация и запуск Telegram бота"""
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from app.bot.handlers import (
    start_command,
    help_command,
    parse_command,
    cities_command,
    app_command,
    error_handler
)

logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None:
    """Инициализация после создания приложения"""
    # Устанавливаем URL Mini App
    web_app_url = os.getenv("WEB_APP_URL", "https://your-frontend-url.com")
    application.bot_data['web_app_url'] = web_app_url
    logger.info(f"Web App URL установлен: {web_app_url}")

def create_bot_application() -> Application:
    """Создает и настраивает приложение бота"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")
    
    # Создаем приложение
    application = Application.builder().token(token).post_init(post_init).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("parse", parse_command))
    application.add_handler(CommandHandler("cities", cities_command))
    application.add_handler(CommandHandler("app", app_command))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    return application

async def start_bot():
    """Запускает бота в режиме polling"""
    application = create_bot_application()
    
    logger.info("Запуск Telegram бота...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )
    
    logger.info("Бот запущен и готов к работе!")
    
    # Ожидание остановки
    await application.updater.stop()
    await application.stop()
    await application.shutdown()

def get_bot_application() -> Application:
    """Получить экземпляр приложения бота (для вебхуков)"""
    return create_bot_application()

