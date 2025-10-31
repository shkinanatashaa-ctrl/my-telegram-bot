import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

print("=== БОТ ЗАПУСКАЕТСЯ ===")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@shkina_design"
CHANNEL_CHAT_ID = "-1002252990214"
WELCOME_IMAGE_URL = "https://i.postimg.cc/DzSnYfxS/photo-2025-10-30-21-09-06.jpg"

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_CHAT_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print(f"Пользователь {user_id} запустил бота")
    
    welcome_text = "💖 Привет! Это Наташа Шкина\nГрафический дизайнер и бьюти-маркетолог\n\nПодпишись на канал и получи список из 30+ небанальных подарков для клиентов!"
    
    try:
        await update.message.reply_photo(photo=WELCOME_IMAGE_URL, caption=welcome_text)
        print("Картинка отправлена")
    except Exception as e:
        print(f"Ошибка картинки: {e}")
        await update.message.reply_text(welcome_text)
    
    if await check_subscription(user_id, context):
        await update.message.reply_text("💖 Спасибо за подписку! Тебе доступны бесплатные материалы! 🎀")
        print(f"Пользователь {user_id} подписан")
    else:
        keyboard = [
            [InlineKeyboardButton("💌 Подписаться на канал", url="https://t.me/shkina_design")],
            [InlineKeyboardButton("🌸 Я подписался", callback_data="check")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎁 Получить список подарков!", reply_markup=reply_markup)
        print(f"Пользователь {user_id} не подписан")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    print(f"Пользователь {user_id} нажал кнопку")
    
    if await check_subscription(user_id, context):
        await query.edit_message_text("💖 Отлично! Теперь у тебя есть доступ к списку из 30+ небанальных подарков для клиентов! 🎀")
        print(f"Подписка {user_id} подтверждена")
    else:
        await query.edit_message_text("💔 Не вижу твоей подписки, попробуй ещё раз 🌸")
        print(f"Подписка {user_id} не найдена")

async def main():
    print("=== ЗАПУСК ПРИЛОЖЕНИЯ ===")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="check"))
    print("=== БОТ ЗАПУЩЕН И РАБОТАЕТ! ===")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
