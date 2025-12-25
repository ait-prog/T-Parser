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

Привет! Я помогу тебе парсить объявления с krisha\.kz

*Доступные команды:*
/start \- Начать работу
/help \- Помощь
/parse \<url\> \- Спарсить страницу krisha\.kz
/cities \- Список доступных городов
/app \- Открыть Mini App

*Пример использования:*
`/parse https://krisha.kz/arenda/kvartiry/almaty/`

Или используй кнопку ниже для открытия Mini App с графиками и картами 📊🗺️
    """
    
    # Кнопка для открытия Mini App
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Открыть Mini App",
            web_app=WebAppInfo(url=context.bot_data.get('web_app_url', 'https://your-frontend-url.com'))
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📖 *Помощь по использованию бота*

*Команды:*

/start \- Начать работу с ботом
/parse \<url\> \- Парсинг страницы krisha\.kz
  Пример: `/parse https://krisha.kz/arenda/kvartiry/almaty/`
  
/cities \- Показать список доступных городов
/app \- Открыть Mini App

*Как использовать:*
1\. Скопируй URL страницы с объявлениями на krisha\.kz
2\. Отправь команду `/parse` с URL
3\. Бот вернет список найденных объявлений

*Mini App:*
Нажми кнопку "Открыть Mini App" для доступа к:
• Графикам и статистике
• Интерактивным картам
• Расширенному поиску по городам и районам
    """
    
    await update.message.reply_text(help_text, parse_mode='MarkdownV2')

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

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /app - открытие Mini App"""
    web_app_url = context.bot_data.get('web_app_url', 'https://your-frontend-url.com')
    
    keyboard = [[InlineKeyboardButton(
        "🚀 Открыть Mini App",
        web_app=WebAppInfo(url=web_app_url)
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🚀 Нажми кнопку ниже для открытия Mini App с графиками, картами и расширенным поиском",
        reply_markup=reply_markup
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ Произошла ошибка\. Попробуй позже или используй команду /help",
            parse_mode='MarkdownV2'
        )

