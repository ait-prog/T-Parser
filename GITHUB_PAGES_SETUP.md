# Настройка GitHub Pages для T-Parser

## Проблема
После деплоя на https://ait-prog.github.io/T-Parser/ показывается README вместо приложения.

## Решение (выполните по порядку)

### Шаг 1: Настройка GitHub Pages в репозитории

1. Зайдите в репозиторий: https://github.com/ait-prog/T-Parser
2. Перейдите в **Settings** (настройки репозитория)
3. В левом меню найдите **Pages**
4. В разделе **Source** выберите:
   - **Source**: `GitHub Actions` (новый способ)
   
   ИЛИ если GitHub Actions не доступен:
   - **Source**: `Deploy from a branch`
   - **Branch**: `gh-pages` → `/ (root)`

### Шаг 2: Запуск GitHub Actions workflow

1. Перейдите во вкладку **Actions** в репозитории
2. В левом меню выберите **Deploy Frontend to GitHub Pages**
3. Если workflow не запустился автоматически:
   - Нажмите **Run workflow**
   - Выберите ветку `main`
   - Нажмите **Run workflow**

### Шаг 3: Ожидание деплоя

1. Дождитесь завершения workflow (обычно 2-5 минут)
2. Проверьте статус в **Actions** - должен быть зеленый чекмарк ✅
3. После успешного деплоя подождите 1-2 минуты для обновления GitHub Pages

### Шаг 4: Проверка

Откройте: https://ait-prog.github.io/T-Parser/

Должно отображаться приложение, а не README.

## Если проблема сохраняется

### Вариант 1: Проверьте workflow логи

1. Зайдите в **Actions** → выберите последний запуск
2. Проверьте, что все шаги выполнены успешно
3. Особенно проверьте шаг "Build" - там не должно быть ошибок

### Вариант 2: Ручной деплой через gh-pages ветку

Если GitHub Actions не работает, можно использовать старый способ:

```bash
cd frontend
npm install
npm run build
npx gh-pages -d out -t true
```

Но это требует установки `gh-pages` пакета.

### Вариант 3: Использование Vercel (рекомендуется)

Vercel лучше подходит для Next.js приложений:

1. Зайдите на https://vercel.com
2. Импортируйте репозиторий `ait-prog/T-Parser`
3. Настройки:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
   - **Environment Variables**: 
     - `NEXT_PUBLIC_API_URL` = ваш URL бэкенда
4. Деплой автоматический

## Текущий статус

После push изменений:
- ✅ Обновлен workflow для GitHub Pages
- ✅ Добавлен `basePath: '/T-Parser'` в next.config.js
- ✅ Добавлен `.nojekyll` файл
- ✅ Workflow использует новый GitHub Actions Pages API

**Следующий шаг**: Настройте GitHub Pages в Settings → Pages → Source: GitHub Actions

