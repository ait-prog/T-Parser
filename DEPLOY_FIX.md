# Исправление проблемы с деплоем на GitHub Pages

## Проблема
GitHub Pages показывает README вместо приложения после деплоя.

## Что было исправлено

### 1. GitHub Actions Workflow (`.github/workflows/deploy.yml`)
- ✅ Убрана зависимость от `package-lock.json` (используется `npm install` вместо `npm ci`)
- ✅ Улучшена проверка build output
- ✅ Улучшено создание `.nojekyll` файла
- ✅ Добавлено логирование для отладки

### 2. Next.js конфигурация (`frontend/next.config.js`)
- ✅ Улучшена логика определения `basePath` для GitHub Actions
- ✅ Добавлена поддержка переменной `GITHUB_ACTIONS` для автоматического определения production режима
- ✅ Добавлено подробное логирование конфигурации

## Шаги для исправления деплоя

### Шаг 1: Убедитесь, что изменения закоммичены и запушены

```bash
git add .
git commit -m "Fix: Исправлен workflow и конфигурация Next.js для GitHub Pages"
git push origin main
```

### Шаг 2: Настройте GitHub Pages в репозитории

1. Откройте: https://github.com/ait-prog/T-Parser/settings/pages
2. В разделе **Build and deployment**:
   - **Source**: выберите **GitHub Actions**
3. Сохраните изменения

**ВАЖНО**: Если опция "GitHub Actions" недоступна:
- Убедитесь, что workflow файл `.github/workflows/deploy.yml` существует в репозитории
- Проверьте, что у репозитория есть права на GitHub Pages

### Шаг 3: Запустите workflow вручную

1. Откройте: https://github.com/ait-prog/T-Parser/actions
2. В левом меню выберите **"Deploy Frontend to GitHub Pages"**
3. Нажмите **"Run workflow"** (справа вверху)
4. Выберите ветку **main**
5. Нажмите **"Run workflow"**

### Шаг 4: Проверьте выполнение workflow

1. Дождитесь завершения workflow (обычно 2-5 минут)
2. Проверьте, что все шаги выполнены успешно (зеленые чекмарки ✅)
3. Особенно проверьте:
   - **Install dependencies** - должен завершиться без ошибок
   - **Build** - должен успешно собрать проект
   - **Verify build output** - должен показать `✅ index.html found`
   - **Deploy to GitHub Pages** - должен успешно задеплоить

### Шаг 5: Проверка результата

После успешного деплоя подождите 1-2 минуты и откройте:
**https://ait-prog.github.io/T-Parser/**

**Должно показывать приложение, а не README!**

## Если проблема сохраняется

### Вариант A: Проверьте логи workflow

1. Зайдите в **Actions** → выберите последний запуск
2. Откройте каждый шаг и проверьте логи:
   - Если ошибка в **Install dependencies**: проверьте `package.json`
   - Если ошибка в **Build**: проверьте логи сборки Next.js
   - Если ошибка в **Verify build output**: проверьте, что `out/index.html` создается
   - Если ошибка в **Deploy**: проверьте настройки GitHub Pages

### Вариант B: Проверьте настройки репозитория

1. Убедитесь, что в **Settings → Pages** выбран источник **GitHub Actions**
2. Проверьте, что у репозитория включен GitHub Pages
3. Убедитесь, что workflow имеет необходимые права (pages: write, id-token: write)

### Вариант C: Локальная проверка сборки

Проверьте, что сборка работает локально:

```bash
cd frontend
npm install
NODE_ENV=production npm run build
ls -la out/
```

Должен быть создан файл `out/index.html` и директория `out/`.

### Вариант D: Альтернативное решение - Vercel

Если GitHub Pages продолжает вызывать проблемы, используйте Vercel (лучше подходит для Next.js):

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

## Технические детали исправлений

### Workflow изменения:
- Убрана зависимость от `package-lock.json` для более гибкой установки зависимостей
- Улучшена обработка ошибок в шаге проверки build output
- Добавлено более подробное логирование

### Next.js конфигурация:
- Автоматическое определение production режима в GitHub Actions через `GITHUB_ACTIONS`
- Поддержка кастомного basePath через переменную `GITHUB_PAGES_BASE_PATH`
- Подробное логирование конфигурации для отладки

## Контакты и поддержка

Если проблема не решена после выполнения всех шагов:
1. Проверьте логи workflow в Actions
2. Убедитесь, что все файлы закоммичены и запушены
3. Проверьте настройки GitHub Pages в Settings

