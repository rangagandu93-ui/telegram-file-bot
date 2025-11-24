import os
import telebot
import threading
import time

# ENV variable se token read karega
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Sirf tum upload kar sako
ADMIN_ID = 8057485206  # <-- Yaha apna Telegram numeric ID daalna

# Temporary storage
stored_files = []  # List of file_ids

# Send all files to user
def send_all_files(chat_id):
    if not stored_files:
        bot.send_message(chat_id, "❌ Abhi koi video available nahi hai.")
        return

    bot.send_message(chat_id, "📁 Aapke liye videos yaha hain:")

    for file_id in stored_files:
        bot.send_video(chat_id, file_id)

    bot.send_message(chat_id, "⏳ Yeh videos 15 minutes me auto-delete ho jayengi.")

# Auto delete function
def auto_delete():
    global stored_files
    time.sleep(900)  # 900 seconds = 15 minutes
    stored_files = []
    print("Files deleted automatically!")


# START Command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
    "🤖 Bot Online!\n\n"
    "Agar videos available hongi to main bhej dunga."
    )


# ADMIN Upload Handler
@bot.message_handler(content_types=['video'])
def handle_video(message):
    global stored_files

    # Check admin
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Aapko upload karne ki permission nahi hai.")
        return

    file_id = message.video.file_id
    stored_files.append(file_id)

    bot.reply_to(message, "✅ Video saved!")

    # Start auto delete thread only once (jab first video aaye)
    if len(stored_files) == 1:
        threading.Thread(target=auto_delete).start()


# Public command — sab video bhejne ke liye
@bot.message_handler(commands=['files'])
def get_files(message):
    send_all_files(message.chat.id)


# Run bot
bot.infinity_polling()
