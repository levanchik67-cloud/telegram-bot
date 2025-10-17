print("🤖 Telegram Bot 24/7 - Working Version!")

import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== НАСТРОЙКИ =====
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8442410256:AAH0wvZoiOpTHxAhUE3o4wZ7LQZpnbpRvCc")
ADMIN_CHAT_ID = 5846819259
CHANNEL_USERNAME = "@eggssssi115"

logging.basicConfig(level=logging.INFO)

# ===== ФУНКЦИИ БОТА =====
async def check_subscription(user_id, context):
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['creator', 'administrator', 'member']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"👤 /start от {user.first_name}")

    is_subscribed = await check_subscription(user.id, context)
    if not is_subscribed:
        await update.message.reply_text(f'❌ Подпишись на канал: {CHANNEL_USERNAME}')
        return

    keyboard = [['📸 Фото', '🎥 Видео', '💬 Вопрос']]
    await update.message.reply_text(
        f'Привет {user.first_name}! ✅',
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"📸 Фото от {user.first_name}")

    is_subscribed = await check_subscription(user.id, context)
    if not is_subscribed:
        await update.message.reply_text('❌ Сначала подпишись на канал!')
        return

    await update.message.reply_text('✅ Фото получено!')
    await context.bot.send_message(ADMIN_CHAT_ID, f"📸 Фото от {user.first_name}:")
    await update.message.forward(ADMIN_CHAT_ID)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"🎥 Видео от {user.first_name}")

    is_subscribed = await check_subscription(user.id, context)
    if not is_subscribed:
        await update.message.reply_text('❌ Сначала подпишись на канал!')
        return

    await update.message.reply_text('✅ Видео получено!')
    await context.bot.send_message(ADMIN_CHAT_ID, f"🎥 Видео от {user.first_name}:")
    await update.message.forward(ADMIN_CHAT_ID)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    print(f"💬 Текст от {user.first_name}: {text}")

    is_subscribed = await check_subscription(user.id, context)
    if not is_subscribed:
        await update.message.reply_text('❌ Сначала подпишись на канал!')
        return

    if text == '📸 Фото':
        await update.message.reply_text('Отправь фото 📷')
    elif text == '🎥 Видео':
        await update.message.reply_text('Отправь видео 🎬')
    elif text == '💬 Вопрос':
        await update.message.reply_text('Напиши вопрос ✍️')
    else:
        await update.message.reply_text('✅ Сообщение отправлено!')
        await context.bot.send_message(ADMIN_CHAT_ID, f"💬 Вопрос от {user.first_name}:\n{text}")
        await update.message.forward(ADMIN_CHAT_ID)

# ===== ЗАПУСК БОТА =====
def main():
    print("🔄 Запуск Telegram бота...")
    
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Бот готов к работе 24/7!")
    print("📱 Проверьте в Telegram: /start")
    
    application.run_polling()

if __name__ == '__main__':
    main()
