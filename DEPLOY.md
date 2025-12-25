# Инструкция по деплою

## 1. Push в GitHub

```bash
# Инициализация git (если еще не сделано)
git init

# Добавление remote
git remote add origin https://github.com/ait-prog/T-Parser.git

# Добавление всех файлов
git add .

# Коммит
git commit -m "Initial commit: Krisha.kz Parser TMA"

# Push в main ветку
git branch -M main
git push -u origin main
```

## 2. Деплой бэкенда

### Вариант 1: Railway / Render / Fly.io

1. Подключите репозиторий к платформе
2. Укажите:
   - **Root Directory**: `back`
   - **Start Command**: `python run.py` или `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     TELEGRAM_BOT_TOKEN=8398428554:AAFbvWG_4iwu870yDkqkhS_77Nf3yQpOi9E
     WEB_APP_URL=https://your-frontend-url.vercel.app
     PORT=8000
     ```

### Вариант 2: PythonAnywhere / Heroku

Аналогично, но используйте их специфичные настройки.

## 3. Деплой фронтенда (GitHub Pages / Vercel)

### GitHub Pages (через GitHub Actions)

Создайте файл `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        working-directory: ./frontend
        run: npm install
        
      - name: Build
        working-directory: ./frontend
        run: npm run build
        env:
          NEXT_PUBLIC_API_URL: ${{ secrets.API_URL }}
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/out
```

**Важно**: Для Next.js нужно настроить `output: 'export'` в `next.config.js`

### Vercel (рекомендуется)

1. Зайдите на [vercel.com](https://vercel.com)
2. Импортируйте репозиторий
3. Укажите:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
     ```

## 4. Настройка бота

После деплоя бэкенда:

1. Получите URL вашего бэкенда (например: `https://your-app.railway.app`)
2. Установите webhook:
   ```bash
   curl "https://your-app.railway.app/api/bot/set-webhook?webhook_url=https://your-app.railway.app/api/bot/webhook"
   ```

Или используйте polling режим:
```bash
# На сервере запустите
cd back
python bot_runner.py
```

## 5. Настройка Mini App в Telegram

1. Откройте [@BotFather](https://t.me/BotFather)
2. Используйте команду `/newapp` или `/editapp`
3. Выберите вашего бота
4. Укажите:
   - **Title**: Krisha.kz Parser
   - **Short name**: krisha-parser
   - **Web App URL**: URL вашего фронтенда (Vercel/GitHub Pages)

## 6. Обновление переменных окружения

После деплоя обновите `WEB_APP_URL` в настройках бэкенда на реальный URL фронтенда.

## Структура после деплоя

```
Frontend (Vercel/GitHub Pages) → https://your-frontend.vercel.app
Backend (Railway/Render) → https://your-backend.railway.app
Telegram Bot → @your_bot
```

