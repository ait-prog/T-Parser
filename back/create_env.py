"""Скрипт для создания .env файла"""
import os

env_content = """# Telegram Bot Token
TELEGRAM_BOT_TOKEN=8398428554:AAFbvWG_4iwu870yDkqkhS_77Nf3yQpOi9E

# Настройки сервера
HOST=0.0.0.0
PORT=8000

# URL фронтенда (Mini App)
WEB_APP_URL=https://ait-prog.github.io/T-Parser

# Настройки парсера
VERIFY_SSL=true
BASE_DELAY_MIN=1.1
BASE_DELAY_MAX=2.6
"""

env_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(env_path):
    print(f"[INFO] Файл .env уже существует: {env_path}")
    response = input("Перезаписать? (y/n): ")
    if response.lower() != 'y':
        print("[INFO] Отменено")
        exit(0)

try:
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print(f"[OK] Файл .env создан: {env_path}")
    print("\nСодержимое:")
    print(env_content)
except Exception as e:
    print(f"[ERROR] Ошибка при создании файла: {e}")

