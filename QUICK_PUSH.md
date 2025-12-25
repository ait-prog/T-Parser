# Быстрый Push в GitHub

## Вариант 1: Использовать скрипт (Windows)

Просто запустите:
```bash
push_to_github.bat
```

## Вариант 2: Ручные команды

```bash
# Инициализация (если еще не сделано)
git init

# Добавление remote
git remote add origin https://github.com/ait-prog/T-Parser.git

# Добавление файлов
git add .

# Коммит
git commit -m "Initial commit: Krisha.kz Parser Telegram Mini App"

# Переименование ветки
git branch -M main

# Push
git push -u origin main
```

## После push:

1. ✅ Код будет в GitHub
2. ✅ Настройте GitHub Pages (Settings → Pages → Source: GitHub Actions)
3. ✅ Задеплойте бэкенд на Railway/Render
4. ✅ Подключите бота (см. `SETUP_GITHUB.md`)

