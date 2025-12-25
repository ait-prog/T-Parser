import uvicorn
import os
import logging
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("=" * 50)
    print("Запуск Krisha.kz Parser API")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Telegram Bot Token: {'Установлен' if os.getenv('TELEGRAM_BOT_TOKEN') else 'НЕ НАЙДЕН'}")
    print(f"Web App URL: {os.getenv('WEB_APP_URL', 'Не установлен')}")
    print("=" * 50)
    print()
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

