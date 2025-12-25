"""Отдельный скрипт для запуска бота в режиме polling"""
import asyncio
import logging
import os
from dotenv import load_dotenv
from app.bot.bot import create_bot_application

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

async def main():
    """Главная функция для запуска бота"""
    application = create_bot_application()
    
    logging.info("Запуск Telegram бота в режиме polling...")
    
    # Инициализация и запуск
    await application.initialize()
    await application.start()
    
    # Запуск polling
    await application.updater.start_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True
    )
    
    logging.info("Бот запущен и готов к работе!")
    logging.info("Нажми Ctrl+C для остановки")
    
    # Ожидание остановки
    try:
        await asyncio.Event().wait()  # Бесконечное ожидание
    except KeyboardInterrupt:
        logging.info("Остановка бота...")
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        logging.info("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())

