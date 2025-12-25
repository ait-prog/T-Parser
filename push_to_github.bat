@echo off
echo ====================================
echo Push в GitHub репозиторий
echo ====================================
echo.

REM Инициализация git (если еще не сделано)
if not exist .git (
    echo Инициализация git репозитория...
    git init
)

REM Добавление remote (если еще не добавлен)
git remote remove origin 2>nul
git remote add origin https://github.com/ait-prog/T-Parser.git

REM Добавление всех файлов
echo.
echo Добавление файлов...
git add .

REM Коммит
echo.
echo Создание коммита...
git commit -m "Initial commit: Krisha.kz Parser Telegram Mini App"

REM Переименование ветки в main
git branch -M main

REM Push
echo.
echo Push в GitHub...
git push -u origin main

echo.
echo ====================================
echo Готово! Код отправлен в GitHub
echo ====================================
pause

