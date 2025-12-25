# Krisha.kz Parser - Telegram Mini App

Telegram Mini App для парсинга объявлений с krisha.kz с графиками, инфографикой и картами.

## Структура проекта

```
tma/
├── back/              # Python бэкенд (FastAPI)
│   ├── app/
│   │   ├── main.py           # Главный файл приложения
│   │   ├── parsers/          # Парсеры
│   │   │   └── krisha_parser.py
│   │   └── routers/          # API роутеры
│   │       ├── parser.py     # Парсинг объявлений
│   │       ├── locations.py  # Поиск адресов
│   │       └── maps.py       # Генерация карт (folium)
│   ├── requirements.txt
│   └── run.py
│
└── frontend/          # Next.js фронтенд
    ├── app/
    │   ├── page.tsx          # Главная страница
    │   └── layout.tsx
    ├── components/
    │   ├── SearchBar.tsx     # Поиск и фильтры
    │   ├── StatsCards.tsx    # Статистика
    │   ├── ChartsSection.tsx # Графики
    │   ├── MapSection.tsx    # Карты
    │   └── PropertyList.tsx  # Список объявлений
    └── package.json
```

## Установка и запуск

### Бэкенд (Python)

1. Перейдите в директорию бэкенда:
```bash
cd back
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` (скопируйте из `.env.example`):
```bash
cp .env.example .env
```

5. Запустите сервер:
```bash
python run.py
```

API будет доступен по адресу: `http://localhost:8000`

### Фронтенд (Next.js)

1. Перейдите в директорию фронтенда:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
```

3. Создайте файл `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Запустите dev сервер:
```bash
npm run dev
```

Приложение будет доступно по адресу: `http://localhost:3000`

## API Endpoints

### Парсинг
- `POST /api/parser/scrape` - Парсинг страницы krisha.kz
- `GET /api/parser/scrape?url=...` - Парсинг (GET метод)

### Поиск адресов
- `GET /api/locations/cities?search=...` - Поиск городов
- `GET /api/locations/districts?city=...` - Получить районы города
- `GET /api/locations/search?query=...` - Универсальный поиск

### Карты
- `POST /api/maps/generate` - Генерация карты с маркерами
- `GET /api/maps/view/{map_id}` - Просмотр карты
- `GET /api/maps/city/{city_name}` - Карта города

## Особенности

- ✅ Парсинг объявлений с krisha.kz
- ✅ Поиск по городам и районам (Алматы, Астана и др.)
- ✅ Графики и статистика (Recharts)
- ✅ Интерактивные карты (Folium)
- ✅ Интеграция с Telegram Mini App
- ✅ Адаптивный дизайн

## Технологии

**Бэкенд:**
- FastAPI
- BeautifulSoup4
- Folium (карты)
- Pandas

**Фронтенд:**
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts (графики)
- Telegram WebApp SDK

## Деплой

### Быстрый старт

1. **Push в GitHub:**
   ```bash
   # Windows
   push_to_github.bat
   
   # Linux/Mac
   chmod +x push_to_github.sh
   ./push_to_github.sh
   ```

2. **Деплой бэкенда:**
   - Railway: [railway.app](https://railway.app) - подключите репозиторий, выберите `back` директорию
   - Render: [render.com](https://render.com) - создайте Web Service из `back` директории

3. **Деплой фронтенда:**
   - GitHub Pages: автоматически через GitHub Actions (см. `.github/workflows/deploy.yml`)
   - Vercel: [vercel.com](https://vercel.com) - импортируйте репозиторий, укажите `frontend` директорию

4. **Настройка бота:**
   - Установите webhook после деплоя бэкенда
   - Настройте Mini App URL через @BotFather

Подробные инструкции в `DEPLOY.md` и `SETUP_GITHUB.md`

## Разработка

Для разработки Telegram Mini App:
1. Создайте бота через @BotFather
2. Настройте Web App URL в настройках бота
3. Используйте Telegram Web App для тестирования

## Лицензия

MIT

