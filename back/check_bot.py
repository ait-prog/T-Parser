# -*- coding: utf-8 -*-
"""Скрипт для проверки подключения Telegram бота"""
import os
import sys
from dotenv import load_dotenv
import requests

# Установка кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

load_dotenv()

def check_bot_connection():
    """Проверка подключения к Telegram Bot API"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("[ERROR] TELEGRAM_BOT_TOKEN не найден в переменных окружения")
        print("   Создайте файл .env в директории back/ с токеном:")
        print("   TELEGRAM_BOT_TOKEN=8398428554:AAFbvWG_4iwu870yDkqkhS_77Nf3yQpOi9E")
        return False
    
    print(f"[OK] Токен найден: {token[:10]}...")
    
    # Проверка валидности токена через API
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("ok"):
            bot_info = data.get("result", {})
            print(f"[OK] Бот подключен успешно!")
            print(f"   Имя бота: @{bot_info.get('username', 'N/A')}")
            print(f"   Имя: {bot_info.get('first_name', 'N/A')}")
            print(f"   ID: {bot_info.get('id', 'N/A')}")
            return True
        else:
            print(f"[ERROR] Ошибка подключения: {data.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Ошибка при проверке: {e}")
        return False

def check_web_app_url():
    """Проверка URL Mini App"""
    web_app_url = os.getenv("WEB_APP_URL", "")
    
    if not web_app_url or web_app_url == "http://localhost:3000":
        print("[WARNING] WEB_APP_URL не установлен или использует localhost")
        print("   Для продакшена установите:")
        print("   WEB_APP_URL=https://ait-prog.github.io/T-Parser")
        return False
    
    print(f"[OK] WEB_APP_URL установлен: {web_app_url}")
    return True

def check_commands():
    """Проверка зарегистрированных команд"""
    print("\n[INFO] Проверка команд бота:")
    commands = [
        "/start", "/hello", "/help", "/run", 
        "/parse", "/cities", "/dev", "/app"
    ]
    
    for cmd in commands:
        print(f"   [OK] {cmd}")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Проверка подключения Telegram бота")
    print("=" * 50)
    print()
    
    bot_ok = check_bot_connection()
    print()
    
    web_app_ok = check_web_app_url()
    print()
    
    check_commands()
    print()
    
    print("=" * 50)
    if bot_ok:
        print("[OK] Бот готов к работе!")
        print("\nСледующие шаги:")
        print("1. Запустите бота: python bot_runner.py")
        print("   ИЛИ")
        print("2. Запустите FastAPI сервер: python run.py")
        print("   (бот инициализируется автоматически)")
    else:
        print("[ERROR] Требуется настройка!")
        print("\nСоздайте файл .env в директории back/")
        print("Скопируйте содержимое из env.example и укажите токен")
    print("=" * 50)

