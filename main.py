import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# ⚠️ ЗАМЕНИ ТОЛЬКО ID КАНАЛА НА РЕАЛЬНЫЙ ⚠️
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@shkina_design"
CHANNEL_CHAT_ID = "-1002252990214"  # ⬅️ ЗАМЕНИ НА РЕАЛЬНЫЙ ID!

# 🔗 ССЫЛКА НА КАРТИНКУ (твоя картинка!)
WELCOME_IMAGE_URL = "https://i.postimg.cc/DzSnYfxS/photo-2025-10-30-21-09-06.jpg"

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_CHAT_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # 💕 ПРИВЕТСТВЕННОЕ СООБЩЕНИЕ С КАРТИНКОЙ
    welcome_text = """💖 Привет! Это Наташа Шкина 
графический дизайнер и бьюти-маркетолог

Подпишись на мой канал и получи список из 30+ небанальных подарков для клиентов!"""
    
    try:
        # Отправляем картинку с текстом
        await update.message.reply_photo(
            photo=WELCOME_IMAGE_URL,
            caption=welcome_text
        )
    except Exception as e:
        # Если картинка не загрузилась, отправляем только текст
        logger.error(f"Ошибка загрузки картинки: {e}")
        await update.message.reply_text(welcome_text)
    
    # Проверяем подписку
    if await check_subscription(user_id, context):
        await update.message.reply_text("💖 Спасибо за подписку! Тебе доступно бесплатные материалы! 🎀")
    else:
        keyboard = [
            [InlineKeyboardButton("💌 Подписаться на канал", url="https://t.me/shkina_design")],
            [InlineKeyboardButton("🌸 Я подписался", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎁 Получить список из 30+ небанальных подарков для клиентов!", reply_markup=reply_markup)

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if await check_subscription(user_id, context):
        await query.edit_message_text("💖 Отлично! Теперь у тебя есть доступ к списку из 30+ небанальных подарков для клиентов! 🎀")
    else:
        await query.edit_message_text("💔 Не вижу твоей подписки, попробуй ещё раз 🌸")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="check_subscription"))
    
    print("Бот запущен и работает 24/7! 🚀")
    application.run_polling()

if name == "main":
    main()