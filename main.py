print("🤖 Telegram Bot 24/7 - Render Version!")

import os
import time
import threading
import logging
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== ВЕБ-СЕРВЕР ДЛЯ ПИНГОВ =====
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот активен! Время: " + time.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/ping')
def ping():
    print(f"✅ Пинг получен: {time.strftime('%H:%M:%S')}")
    return "pong"

@app.route('/health')
def health():
    return "healthy"

def run_web():
    print("🌐 Веб-сервер запускается...")
    app.run(host='0.0.0.0', port=5000)

# ===== НАСТРОЙКИ =====
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8442410256:AAEHxB066xzt6BYos99zb7ZKnykvPyWPyv4")
ADMIN_CHAT_ID = 5846819259
CHANNEL_USERNAME = "@eggssssi115"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ===== ФУНКЦИИ БОТА =====
async def check_subscription(user_id, context):
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['creator', 'administrator', 'member', 'restricted']
    except Exception as e:
        print(f"❌ Ошибка проверки подписки: {e}")
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

    await update.message.reply_text('✅ Фото получено! Пересылаю админу...')
    await context.bot.send_message(ADMIN_CHAT_ID, f"📸 Фото от {user.first_name} (@{user.username}):")
    await update.message.forward(ADMIN_CHAT_ID)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"🎥 Видео от {user.first_name}")

    is_subscribed = await check_subscription(user.id, context)
    if not is_subscribed:
        await update.message.reply_text('❌ Сначала подпишись на канал!')
        return

    await update.message.reply_text('✅ Видео получено! Пересылаю админу...')
    await context.bot.send_message(ADMIN_CHAT_ID, f"🎥 Видео от {user.first_name} (@{user.username}):")
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
        await update.message.reply_text('Напиши свой вопрос ✍️')
    else:
        await update.message.reply_text('✅ Сообщение отправлено! Пересылаю админу...')
        await context.bot.send_message(ADMIN_CHAT_ID, f"💬 Вопрос от {user.first_name} (@{user.username}):\n{text}")
        await update.message.forward(ADMIN_CHAT_ID)
# ===== ЗАПУСК БОТА =====
def main():
    print("🔄 Запуск Telegram бота...")
    
    # Запускаем Flask в фоне
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    time.sleep(2)
    print("✅ Веб-сервер запущен на порту 5000")

    # Создаем приложение с правильными настройками
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Бот готов к работе 24/7!")
    print("📱 Проверьте бота в Telegram")
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
