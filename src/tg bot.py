import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


TOKEN = "7866756435:AAGgg7t2LIRufYAecNX18nsIVG6kacf14SM"

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Контакты проекта:\n• Руководитель: @a_harlamenkov\n• Технические вопросы: @klmvika\n🏢 Личный прием:\nАдрес: ул. Большая Семёновская, 38")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n"
        "Я бот проекта *«Автоматизация внутренних бизнес-процессов университета. 2ГИС»*.\n"
        "Здесь ты можешь узнать о проекте, участниках и последних обновлениях.\n\n"
        "Доступные команды:\n"
        "/about - О проекте\n"
        "/team - Участники проекта\n"
        "/tasks - Кто чем занимается\n"
        "/progress - Текущий прогресс\n"
        "/contacts - Контакты проекта",  
        parse_mode="Markdown"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📌 *О проекте:*\n\n"
        "Наш проект создан для удобства студентов и преподавателей Московского Политеха.\n"
        "Мы делаем замеры аудиторий и коридоров всех корпусов, чтобы перенести их в 3D и добавить в 2ГИС.\n\n"
        "🔹 *Цель:*\n"
        "Создать детализированную карту университета, чтобы любой человек мог быстро найти нужную аудиторию.\n\n"
        "🔹 *Как это работает?*\n"
        "1️⃣ Студенты делают замеры помещений\n"
        "2️⃣ Данные переносятся в 3D-модель\n"
        "3️⃣ Готовая модель интегрируется в 2ГИС\n\n"
        "📌 Проект реализуется силами студентов 1 курса.",
        parse_mode="Markdown"
    )


async def team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Лидер проекта", callback_data="leader")],
        [InlineKeyboardButton("Замерщики", callback_data="measurements")],
        [InlineKeyboardButton("3D-моделлер", callback_data="3d")],
        [InlineKeyboardButton("Проджект-менеджер", callback_data="promotion")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👥 *Участники проекта:*\nВыберите категорию:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    query = update.callback_query
    await query.answer()
    
    if query.data == "leader":
        await query.edit_message_text("💼 Лидер проекта:\nАлина\nОтвечает за координацию команды.")
    elif query.data == "measurements":
        await query.edit_message_text("📏 Команда замерщиков:\nВероника, Алина, Марго\nЗанимаются замером корпусов.")
    elif query.data == "3d":
        await query.edit_message_text("🖥️ 3D-моделирование:\nЕвгения, Виктория, Станислав\nСоздают 3D-модель корпусов.")
    elif query.data == "promotion":
        await query.edit_message_text("📢 Проджект-менеджер:\nМихаил\nРассказывает о проекте в соцсетях, контролирует сроки и статус выполнения.")

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📋 *Распределение задач:*\n"
        "• **Лидер** – управление командой\n"
        "• **Замерщики** – сбор данных по аудиториям\n"
        "• **3D-моделлеры** – создание модели\n"
        "• **Менеджеры** – соцсети, презентации, контроль\n\n"
        "Хочешь присоединиться? Напиши /contacts!", 
        parse_mode="Markdown"
    )


async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📊 *Текущий прогресс:*\n\n"
        "✅ Завершено:\n"
        "- Обмерено 4 корпуса (ПК, ПР, БС, МХ)\n"
        "- Создано 90% 3D-модели\n\n"
        "🔄 В работе:\n"
        "- Интеграция с 2ГИС\n"
        "- Фотофиксация помещений\n\n"
        "⏳ Планы:\n"
        "- Завершить проект к [июню]",
        parse_mode="Markdown"
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Извините, такой команды нет. Попробуйте /contacts", 
        parse_mode="Markdown"
    )

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    handlers = [
        CommandHandler("start", start),
        CommandHandler("contacts", contacts),  
        CommandHandler("about", about),
        CommandHandler("team", team),
        CommandHandler("tasks", tasks),
        CommandHandler("progress", progress),
        CallbackQueryHandler(button_handler),
        MessageHandler(
            filters.COMMAND & ~filters.Regex(r'^/(start|contacts|about|team|tasks|progress)'),
            unknown
        )
    ]
    
    for handler in handlers:
        application.add_handler(handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()