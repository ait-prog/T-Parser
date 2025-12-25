#!/bin/bash

echo "===================================="
echo "Push в GitHub репозиторий"
echo "===================================="
echo ""

# Инициализация git (если еще не сделано)
if [ ! -d .git ]; then
    echo "Инициализация git репозитория..."
    git init
fi

# Добавление remote (если еще не добавлен)
git remote remove origin 2>/dev/null
git remote add origin https://github.com/ait-prog/T-Parser.git

# Добавление всех файлов
echo ""
echo "Добавление файлов..."
git add .

# Коммит
echo ""
echo "Создание коммита..."
git commit -m "Initial commit: Krisha.kz Parser Telegram Mini App"

# Переименование ветки в main
git branch -M main

# Push
echo ""
echo "Push в GitHub..."
git push -u origin main

echo ""
echo "===================================="
echo "Готово! Код отправлен в GitHub"
echo "===================================="

