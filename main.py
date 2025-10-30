import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)


BOT_TOKEN = os.getenv(8357525142:AAGH9ibtm3P57lIqVVZPPKm2m4jHwFXuFJI) 
CHANNEL_USERNAME = "@shkina_design"  
CHANNEL_CHAT_ID = "-1002252990214"

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_CHAT_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if await check_subscription(user_id, context):
        await update.message.reply_text("✅ Спасибо за подписку! Тебе доступны бесплатные материалы!")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("❌ Подпишись на канал чтобы получить подарок!", reply_markup=reply_markup)

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if await check_subscription(user_id, context):
        await query.edit_message_text("✅ Отлично! Теперь ты можешь получить бесплатные материалы!")
    else:
        await query.edit_message_text("❌ Ты еще не подписался на канал!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="check_subscription"))
    
    print("Бот запущен и работает 24/7! 🚀")
    application.run_polling()

if name == "main":
    main()