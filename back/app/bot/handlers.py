"""Обработчики команд Telegram бота"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
from app.parsers.krisha_parser import KrishaParser

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
🏠 *Krisha\.kz Parser Bot*

Привет\! Я помогу тебе парсить объявления с krisha\.kz

*Что я умею:*
🔍 Парсить объявления с krisha\.kz
📊 Показывать статистику и графики
🗺️ Отображать объявления на карте
🏙️ Искать по городам и районам

*Быстрый старт:*
1\. Используй команду `/run` для открытия Mini App
2\. Или `/parse` для быстрого парсинга страницы

*Пример:*
`/parse https://krisha.kz/arenda/kvartiry/almaty/`

*Доступные команды:*
/start \- Начать работу
/hello \- Описание бота
/help \- Помощь
/run \- Запустить Mini App
/parse \- Парсинг страницы
/cities \- Список городов
/dev \- Информация об авторе

Используй кнопки ниже для быстрого доступа\! 👇
    """
    
    # Кнопки для быстрого доступа
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Запустить Mini App",
            web_app=WebAppInfo(url=context.bot_data.get('web_app_url', 'https://your-frontend-url.com'))
        )],
        [
            InlineKeyboardButton("👋 Приветствие", callback_data="hello"),
            InlineKeyboardButton("📖 Помощь", callback_data="help")
        ],
        [
            InlineKeyboardButton("🔍 Парсинг", callback_data="parse_help"),
            InlineKeyboardButton("👨‍💻 Автор", callback_data="dev")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup
    )

async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /hello - описание бота"""
    hello_text = """
👋 *Привет\!*

Я *Krisha\.kz Parser Bot* \- умный помощник для работы с объявлениями недвижимости\.

*Что я умею:*
🔍 Парсить объявления с krisha\.kz
📊 Показывать статистику и графики
🗺️ Отображать объявления на карте
🏙️ Искать по городам и районам Казахстана
📈 Анализировать цены и тренды

*Мои возможности:*
• Парсинг страниц с объявлениями
• Фильтрация по городам \(Алматы, Астана, Шымкент и др\.\)
• Поиск по районам
• Визуализация данных на графиках
• Интерактивные карты с маркерами объявлений

*Как начать:*
Используй команду `/run` для открытия Mini App или `/parse` для быстрого парсинга\.

*Пример:*
`/parse https://krisha.kz/arenda/kvartiry/almaty/`

Готов помочь тебе найти идеальное жилье\! 🏡
    """
    
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Запустить Mini App",
            web_app=WebAppInfo(url=context.bot_data.get('web_app_url', 'https://your-frontend-url.com'))
        )],
        [
            InlineKeyboardButton("📖 Помощь", callback_data="help"),
            InlineKeyboardButton("👨‍💻 Автор", callback_data="dev")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        hello_text,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📖 *Помощь по использованию бота*

*Доступные команды:*

/start \- Начать работу с ботом
/hello \- Описание бота и его возможностей
/help \- Показать эту справку
/run \- Запустить Mini App
/parse \<url\> \- Парсинг страницы krisha\.kz
  Пример: `/parse https://krisha.kz/arenda/kvartiry/almaty/`
  
/cities \- Показать список доступных городов
/dev \- Информация об авторе

*Как использовать парсинг:*
1\. Скопируй URL страницы с объявлениями на krisha\.kz
2\. Отправь команду `/parse` с URL
3\. Бот вернет список найденных объявлений с ценами и локациями

*Mini App:*
Используй команду `/run` или кнопку "Запустить Mini App" для доступа к:
• 📊 Графикам и статистике
• 🗺️ Интерактивным картам
• 🔍 Расширенному поиску по городам и районам
• 📈 Аналитике цен

*Поддерживаемые города:*
Алматы, Астана, Шымкент, Караганда и другие крупные города Казахстана

*Нужна помощь?*
Используй команду `/dev` для связи с автором
    """
    
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Запустить Mini App",
            web_app=WebAppInfo(url=context.bot_data.get('web_app_url', 'https://your-frontend-url.com'))
        )],
        [
            InlineKeyboardButton("👋 Приветствие", callback_data="hello"),
            InlineKeyboardButton("👨‍💻 Автор", callback_data="dev")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        help_text,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup
    )

async def parse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /parse"""
    if not context.args:
        await update.message.reply_text(
            "❌ Укажи URL страницы krisha\.kz\n"
            "Пример: `/parse https://krisha.kz/arenda/kvartiry/almaty/`",
            parse_mode='MarkdownV2'
        )
        return
    
    url = ' '.join(context.args)
    
    if 'krisha.kz' not in url:
        await update.message.reply_text(
            "❌ Поддерживаются только ссылки с krisha\.kz",
            parse_mode='MarkdownV2'
        )
        return
    
    # Отправляем сообщение о начале парсинга
    status_msg = await update.message.reply_text("⏳ Парсинг страницы\.\.\.")
    
    try:
        parser = KrishaParser(verify_ssl=True)
        items = parser.parse_url(url)
        
        if not items:
            await status_msg.edit_text("❌ Объявления не найдены")
            return
        
        # Формируем ответ
        result_text = f"✅ Найдено объявлений: *{len(items)}*\n\n"
        
        # Показываем первые 5 объявлений
        for i, item in enumerate(items[:5], 1):
            price = f"{item['price']:,} ₸".replace(",", " ")
            result_text += f"*{i}\. {item['title'][:50]}*\.\.\.\n"
            result_text += f"💰 {price}\n"
            result_text += f"📍 {item['location']}\n"
            if item.get('district') and item['district'] != 'Не указано':
                result_text += f"🏘️ {item['district']}\n"
            result_text += f"[Открыть]({item['url']})\n\n"
        
        if len(items) > 5:
            result_text += f"\.\.\. и еще *{len(items) - 5}* объявлений"
        
        result_text += "\n\n💡 Используй Mini App для просмотра всех объявлений с графиками и картами"
        
        # Кнопка для открытия Mini App
        keyboard = [[InlineKeyboardButton(
            "🚀 Открыть Mini App",
            web_app=WebAppInfo(url=context.bot_data.get('web_app_url', 'https://your-frontend-url.com'))
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await status_msg.edit_text(
            result_text,
            parse_mode='MarkdownV2',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        await status_msg.edit_text(
            f"❌ Ошибка при парсинге: {str(e)}",
            parse_mode='MarkdownV2'
        )

async def cities_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /cities"""
    from app.routers.locations import CITIES_DATA
    
    cities_text = "🏙️ *Доступные города:*\n\n"
    
    for city_name, city_data in CITIES_DATA.items():
        cities_text += f"*{city_data['name']}*\n"
        cities_text += f"Районов: {len(city_data['districts'])}\n"
        if city_data['name_alt']:
            cities_text += f"Альтернативные названия: {', '.join(city_data['name_alt'])}\n"
        cities_text += "\n"
    
    cities_text += "💡 Используй Mini App для поиска по городам и районам"
    
    keyboard = [[InlineKeyboardButton(
        "🚀 Открыть Mini App",
        web_app=WebAppInfo(url=context.bot_data.get('web_app_url', 'https://your-frontend-url.com'))
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        cities_text,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup
    )

async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /run - запуск Mini App"""
    web_app_url = context.bot_data.get('web_app_url', 'https://your-frontend-url.com')
    
    run_text = """
🚀 *Запуск Mini App*

Нажми кнопку ниже для открытия полнофункционального приложения с:

📊 *Графиками и статистикой*
• Распределение по городам
• Анализ цен
• Статистика по районам

🗺️ *Интерактивными картами*
• Визуализация объявлений на карте
• Поиск по локациям

🔍 *Расширенным поиском*
• Фильтры по городам
• Поиск по районам
• Детальная информация

*Готов начать\!* Нажми кнопку ниже 👇
    """
    
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Открыть Mini App",
            web_app=WebAppInfo(url=web_app_url)
        )],
        [
            InlineKeyboardButton("📖 Помощь", callback_data="help"),
            InlineKeyboardButton("👨‍💻 Автор", callback_data="dev")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        run_text,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup
    )

async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /dev - информация об авторе"""
    dev_text = """
👨‍💻 *Информация об авторе*

*Разработчик:* ait\-prog

*Проект:* Krisha\.kz Parser Telegram Mini App

*Технологии:*
• Python \(FastAPI\)
• Next\.js \(TypeScript\)
• Telegram Bot API
• Folium для карт
• Recharts для графиков

*Возможности проекта:*
✅ Парсинг объявлений с krisha\.kz
✅ Визуализация данных
✅ Интерактивные карты
✅ Поиск по городам и районам
✅ Telegram Mini App интеграция

*GitHub:* [ait\-prog/T\-Parser](https://github.com/ait-prog/T-Parser)

*Страница проекта:*
[GitHub Pages](https://ait-prog.github.io/T-Parser/)

Спасибо за использование бота\! 🙏
    """
    
    keyboard = [
        [
            InlineKeyboardButton("🔗 GitHub", url="https://github.com/ait-prog/T-Parser"),
            InlineKeyboardButton("🌐 GitHub Pages", url="https://ait-prog.github.io/T-Parser/")
        ],
        [
            InlineKeyboardButton("🚀 Запустить Mini App", web_app=WebAppInfo(
                url=context.bot_data.get('web_app_url', 'https://your-frontend-url.com')
            ))
        ],
        [
            InlineKeyboardButton("📖 Помощь", callback_data="help"),
            InlineKeyboardButton("👋 Приветствие", callback_data="hello")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        dev_text,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /app - открытие Mini App (алиас для /run)"""
    await run_command(update, context)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback кнопок"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        # Создаем временный update для команды
        temp_update = Update(
            update_id=update.update_id,
            message=query.message
        )
        await help_command(temp_update, context)
    elif query.data == "hello":
        temp_update = Update(
            update_id=update.update_id,
            message=query.message
        )
        await hello_command(temp_update, context)
    elif query.data == "dev":
        temp_update = Update(
            update_id=update.update_id,
            message=query.message
        )
        await dev_command(temp_update, context)
    elif query.data == "parse_help":
        await query.message.reply_text(
            "📝 *Как использовать парсинг:*\n\n"
            "1\. Скопируй URL страницы с krisha\.kz\n"
            "2\. Отправь команду `/parse` с URL\n"
            "3\. Бот вернет список объявлений\n\n"
            "*Пример:*\n"
            "`/parse https://krisha.kz/arenda/kvartiry/almaty/`\n\n"
            "💡 Или используй Mini App для расширенных возможностей\!",
            parse_mode='MarkdownV2'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ Произошла ошибка\. Попробуй позже или используй команду /help",
            parse_mode='MarkdownV2'
        )

