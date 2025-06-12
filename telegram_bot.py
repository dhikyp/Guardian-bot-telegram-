from flask import Flask
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatPermissions
import re

# TOKEN API BOT kamu
TOKEN = "8160234854:AAFqXWBi6RpZ3CBXSqt9n7Sxb-vqV9C_4dM"

# Daftar keyword spam/phishing
SPAM_KEYWORDS = [
    "airdrop", "bonus", "click here", "free", "claim now", "http", "https", "t.me/", "binance", "pump"
]

# Fungsi /start
def start(update, context):
    update.message.reply_text("✅ Bot aktif! Siap menjaga grup dari spam dan link phishing.")

# Fungsi mendeteksi spam dan hapus pesan
def check_message(update, context):
    message = update.message
    text = message.text.lower() if message.text else ""

    # Deteksi link atau kata mencurigakan
    if any(keyword in text for keyword in SPAM_KEYWORDS) or re.search(r'https?://\S+', text):
        try:
            context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
            print(f"Pesan spam dihapus: {text}")
        except Exception as e:
            print(f"Gagal hapus pesan: {e}")

# Flask webserver (agar bisa di-ping uptime robot)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Main bot setup
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Perintah /start
    dp.add_handler(CommandHandler("start", start))

    # Handler untuk cek dan hapus pesan spam
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))

    # Aktifkan webserver dan polling
    keep_alive()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()