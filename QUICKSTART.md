# Быстрый старт

## 1. Запуск бэкенда

```bash
cd back
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac  
source venv/bin/activate

pip install -r requirements.txt
python run.py
```

Бэкенд запустится на `http://localhost:8000`

## 2. Запуск фронтенда

В новом терминале:

```bash
cd frontend
npm install
npm run dev
```

Фронтенд запустится на `http://localhost:3000`

## 3. Использование

1. Откройте `http://localhost:3000` в браузере
2. Вставьте URL страницы krisha.kz (например: `https://krisha.kz/arenda/kvartiry/almaty/`)
3. Нажмите "Спарсить"
4. Просмотрите результаты, графики и карту

## 4. Telegram Mini App

Для тестирования в Telegram:
1. Создайте бота через @BotFather
2. Используйте команду `/newapp` для создания Mini App
3. Укажите URL вашего фронтенда (например, ngrok или другой хостинг)
4. Откройте бота в Telegram и нажмите на кнопку Mini App

## API Документация

После запуска бэкенда доступна автоматическая документация:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

