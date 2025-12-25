# Быстрая настройка GitHub репозитория

## Шаг 1: Инициализация и Push

```bash
# Перейдите в корневую директорию проекта
cd d:\CSS 330\tma

# Инициализация git (если еще не сделано)
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "Initial commit: Krisha.kz Parser Telegram Mini App"

# Добавление remote репозитория
git remote add origin https://github.com/ait-prog/T-Parser.git

# Переименование ветки в main (если нужно)
git branch -M main

# Push в репозиторий
git push -u origin main
```

## Шаг 2: Настройка GitHub Pages

1. Зайдите в настройки репозитория: `Settings` → `Pages`
2. В разделе `Source` выберите:
   - **Source**: `GitHub Actions`
3. Сохраните

## Шаг 3: Настройка Secrets для GitHub Actions

1. Зайдите в `Settings` → `Secrets and variables` → `Actions`
2. Добавьте секреты:
   - `NEXT_PUBLIC_API_URL` - URL вашего бэкенда (после деплоя)

## Шаг 4: Деплой бэкенда

### Railway (рекомендуется)

1. Зайдите на [railway.app](https://railway.app)
2. Создайте новый проект
3. Подключите GitHub репозиторий
4. Выберите `back` директорию
5. Установите переменные окружения:
   ```
   TELEGRAM_BOT_TOKEN=8398428554:AAFbvWG_4iwu870yDkqkhS_77Nf3yQpOi9E
   WEB_APP_URL=https://your-username.github.io/T-Parser
   PORT=8000
   ```
6. Railway автоматически задеплоит

### Render

1. Зайдите на [render.com](https://render.com)
2. Создайте новый Web Service
3. Подключите GitHub репозиторий
4. Настройки:
   - **Root Directory**: `back`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
5. Добавьте переменные окружения (как выше)

## Шаг 5: Обновление URL в GitHub Secrets

После деплоя бэкенда:
1. Скопируйте URL бэкенда (например: `https://your-app.railway.app`)
2. Обновите секрет `NEXT_PUBLIC_API_URL` в GitHub
3. Перезапустите GitHub Actions workflow

## Шаг 6: Настройка Telegram Bot

1. После деплоя бэкенда установите webhook:
   ```bash
   curl "https://your-backend.railway.app/api/bot/set-webhook?webhook_url=https://your-backend.railway.app/api/bot/webhook"
   ```

2. Настройте Mini App через @BotFather:
   - `/newapp` или `/editapp`
   - Выберите бота
   - **Web App URL**: `https://your-username.github.io/T-Parser`

## Готово! 🎉

Теперь у вас:
- ✅ Код в GitHub
- ✅ Фронтенд на GitHub Pages
- ✅ Бэкенд на Railway/Render
- ✅ Telegram бот подключен

