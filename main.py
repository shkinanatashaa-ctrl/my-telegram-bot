import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@shkina_design"
CHANNEL_CHAT_ID = "-1002252990214"  # ✅ ТВОЙ ID КАНАЛА
WELCOME_IMAGE_URL = "https://i.postimg.cc/DzSnYfxS/photo-2025-10-30-21-09-06.jpg"

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_CHAT_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

async def start(update, context):
    user_id = update.effective_user.id
    
    welcome_text = "💖 Привет! Это Наташа Шкина\nГрафический дизайнер и бьюти-маркетолог\n\nПодпишись на канал и получи список из 30+ небанальных подарков для клиентов!"
    
    try:
        await update.message.reply_photo(
            photo=WELCOME_IMAGE_URL,
            caption=welcome_text
        )
    except Exception as e:
        await update.message.reply_text(welcome_text)
    
    if await check_subscription(user_id, context):
        await update.message.reply_text("💖 Спасибо за подписку! Тебе доступны бесплатные материалы!")
    else:
        keyboard = [
            [InlineKeyboardButton("💌 Подписаться на канал", url="https://t.me/shkina_design")],
            [InlineKeyboardButton("🌸 Я подписался", callback_data="check")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎁 Получить список подарков!", reply_markup=reply_markup)

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if await check_subscription(user_id, context):
        await query.edit_message_text("💖 Отлично! Теперь у тебя есть доступ к списку из 30+ небанальных подарков!")
    else:
        await query.edit_message_text("💔 Не вижу твоей подписки, попробуй ещё раз")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="check"))
    print("Bot started!")
    application.run_polling()

if name == "main":
    main()