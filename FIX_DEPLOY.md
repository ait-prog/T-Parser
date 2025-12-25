# Исправление деплоя на GitHub Pages

## Проблема
GitHub Pages показывает README вместо приложения.

## Решение

### 1. Настройка GitHub Pages

1. Зайдите в репозиторий: https://github.com/ait-prog/T-Parser
2. Перейдите в **Settings** → **Pages**
3. В разделе **Source** выберите:
   - **Source**: `Deploy from a branch`
   - **Branch**: `gh-pages` → `/ (root)`
   
   ИЛИ (новый способ):
   - **Source**: `GitHub Actions`

### 2. Запуск workflow вручную

1. Перейдите в **Actions** вкладку репозитория
2. Выберите workflow "Deploy Frontend to GitHub Pages"
3. Нажмите **Run workflow** → **Run workflow**

### 3. Альтернативное решение (если Actions не работает)

Создайте файл `.nojekyll` в корне репозитория и используйте старый способ:

```bash
# В корне репозитория создайте .nojekyll
touch .nojekyll
git add .nojekyll
git commit -m "Add .nojekyll for GitHub Pages"
git push
```

Затем в Settings → Pages выберите:
- **Source**: `Deploy from a branch`
- **Branch**: `main` → `/frontend/out`

### 4. Проверка

После деплоя проверьте:
- https://ait-prog.github.io/T-Parser/ должен показывать приложение
- В Actions должна быть успешная сборка
- В Settings → Pages должен быть указан правильный источник

## Если проблема сохраняется

1. Убедитесь, что `basePath: '/T-Parser'` в `next.config.js`
2. Проверьте, что workflow запускается и завершается успешно
3. Убедитесь, что в Settings → Pages выбран правильный источник (GitHub Actions)

