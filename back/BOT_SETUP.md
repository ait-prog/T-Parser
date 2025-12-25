# Настройка Telegram бота

## 1. Получение токена

Токен уже получен: `8398428554:AAFbvWG_4iwu870yDkqkhS_77Nf3yQpOi9E`

## 2. Настройка переменных окружения

Создайте файл `.env` в директории `back/` (скопируйте из `env.example`):

```bash
TELEGRAM_BOT_TOKEN=8398428554:AAFbvWG_4iwu870yDkqkhS_77Nf3yQpOi9E
WEB_APP_URL=http://localhost:3000
HOST=0.0.0.0
PORT=8000
```

## 3. Запуск бота

### Вариант 1: Polling (для разработки)

Запустите бота отдельно в режиме polling:

```bash
cd back
python bot_runner.py
```

### Вариант 2: Интеграция с FastAPI (для вебхуков)

Бот автоматически инициализируется при запуске FastAPI сервера:

```bash
cd back
python run.py
```

Затем установите webhook:

```bash
curl "http://localhost:8000/api/bot/set-webhook?webhook_url=https://your-domain.com/api/bot/webhook"
```

## 4. Команды бота

- `/start` - Начать работу с ботом
- `/help` - Помощь
- `/parse <url>` - Спарсить страницу krisha.kz
- `/cities` - Список доступных городов
- `/app` - Открыть Mini App

## 5. Настройка Mini App

1. Откройте бота в Telegram
2. Используйте команду `/app` или кнопку "Открыть Mini App"
3. Убедитесь, что `WEB_APP_URL` указывает на ваш фронтенд

## 6. Пример использования

```
/parse https://krisha.kz/arenda/kvartiry/almaty/
```

Бот вернет список найденных объявлений с возможностью открыть Mini App для просмотра графиков и карт.

