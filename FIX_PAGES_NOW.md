# СРОЧНОЕ ИСПРАВЛЕНИЕ GitHub Pages

## Проблема
GitHub Pages показывает README вместо приложения.

## Решение (выполните ВСЕ шаги):

### Шаг 1: Настройка GitHub Pages в репозитории

1. Откройте: https://github.com/ait-prog/T-Parser/settings/pages
2. В разделе **Build and deployment**:
   - **Source**: выберите **GitHub Actions**
3. Сохраните изменения

### Шаг 2: Удаление старой ветки gh-pages (если есть)

```bash
# В терминале GitHub или локально:
git push origin --delete gh-pages
```

### Шаг 3: Запуск workflow вручную

1. Откройте: https://github.com/ait-prog/T-Parser/actions
2. В левом меню выберите **"Deploy Frontend to GitHub Pages"**
3. Нажмите **"Run workflow"** (справа вверху)
4. Выберите ветку **main**
5. Нажмите **"Run workflow"**

### Шаг 4: Ожидание деплоя

1. Дождитесь завершения workflow (2-5 минут)
2. Проверьте, что все шаги зеленые ✅
3. Особенно проверьте шаг "Verify build output" - должен показать `✅ index.html found`

### Шаг 5: Проверка результата

После успешного деплоя подождите 1-2 минуты и откройте:
https://ait-prog.github.io/T-Parser/

**Должно показывать приложение, а не README!**

## Если все еще показывает README:

### Вариант A: Проверьте логи workflow

1. Зайдите в **Actions** → последний запуск
2. Откройте шаг **"Build"**
3. Проверьте шаг **"Verify build output"**
4. Если там ошибка - сообщите, что именно

### Вариант B: Альтернативный способ (если Actions не работает)

1. В Settings → Pages измените:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main`
   - **Folder**: `/frontend/out`

2. Но это требует, чтобы `frontend/out` был в репозитории (что не рекомендуется)

### Вариант C: Использование Vercel (рекомендуется)

Vercel лучше работает с Next.js:

1. Зайдите на https://vercel.com
2. Импортируйте репозиторий `ait-prog/T-Parser`
3. Настройки:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `out`
   - **Environment Variables**:
     - `NEXT_PUBLIC_API_URL` = ваш URL бэкенда
4. Деплой автоматический

## Текущие изменения:

✅ Обновлен workflow с проверкой build output
✅ Улучшена конфигурация next.config.js
✅ Добавлен .nojekyll файл
✅ Добавлена проверка наличия index.html

**ВАЖНО**: После изменений обязательно:
1. Настройте GitHub Pages на **GitHub Actions**
2. Запустите workflow вручную
3. Дождитесь завершения

