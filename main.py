import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования - ВАЖНО: две черты с двух сторон!
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)  # ⚠️ ДВЕ ЧЕРТЫ: __name__

# Данные бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@shkina_design"
CHANNEL_CHAT_ID = "-1002252990214"
WELCOME_IMAGE_URL = "https://i.postimg.cc/DzSnYfxS/photo-2025-10-30-21-09-06.jpg"

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_CHAT_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        
        welcome_text = """💖 Привет! Это Наташа Шкина 
Графический дизайнер и бьюти-маркетолог

Подпишись на канал и получи список из 30+ небанальных подарков для клиентов!"""
        
        # Пытаемся отправить картинку
        try:
            await update.message.reply_photo(
                photo=WELCOME_IMAGE_URL,
                caption=welcome_text
            )
            logger.info("Картинка отправлена успешно")
        except Exception as e:
            logger.warning(f"Не удалось отправить картинку: {e}")
            await update.message.reply_text(welcome_text)
        
        # Проверяем подписку
        if await check_subscription(user_id, context):
            await update.message.reply_text("💖 Спасибо за подписку! Тебе доступны бесплатные материалы! 🎀")
            logger.info(f"Пользователь {user_id} уже подписан")
        else:
            keyboard = [
                [InlineKeyboardButton("💌 Подписаться на канал", url="https://t.me/shkina_design")],
                [InlineKeyboardButton("🌸 Я подписался", callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("🎁 Получить список из 30+ небанальных подарков для клиентов!", reply_markup=reply_markup)
            logger.info(f"Пользователь {user_id} не подписан, показаны кнопки")
            
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        logger.info(f"Пользователь {user_id} нажал кнопку проверки подписки")
        
        if await check_subscription(user_id, context):
            await query.edit_message_text("💖 Отлично! Теперь у тебя есть доступ к списку из 30+ небанальных подарков для клиентов! 🎀")
            logger.info(f"Подписка пользователя {user_id} подтверждена")
        else:
            await query.edit_message_text("💔 Не вижу твоей подписки, попробуй ещё раз 🌸")
            logger.info(f"Подписка пользователя {user_id} не найдена")
            
    except Exception as e:
        logger.error(f"Ошибка в обработчике кнопки: {e}")

def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="check_subscription"))
        
        logger.info("🤖 Бот запускается...")
        application.run_polling()
        logger.info("✅ Бот успешно запущен и работает!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()