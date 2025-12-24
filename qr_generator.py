import telebot
import qrcode
import os

# Configuration
TOKEN = "8351679772:AAGFIE07ZVY7z55erijuN76visCu7APsKyA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username
    name = f"@{username}" if username else message.from_user.first_name
    welcome_text = (
        f"ជំរាបសូរ{name}!\n\n"
        "សូមស្វាគមន៍មកកាន់ប្រព័ន្ធបង្កើត QR Code!\n"
        "សូមផ្ញើតំណភ្ជាប់ ឬអត្ថបទណាមួយមកខ្ញុំ ខ្ញុំនឹងបង្កើត QR code ជូនអ្នក។"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def generate_qr_from_text(message):
    text = message.text
    if not text:
        return

    username = message.from_user.username
    name = f"@{username}" if username else message.from_user.first_name

    # Generate QR Code
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"qr_{message.chat.id}.png"
        img.save(filename)

        # Send Photo
        caption = f"ជំរាបសូរ {name} 👌\nនេះគឺជា QR code សម្រាប់៖\n{text}"
        with open(filename, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=caption)
        
        # Clean up
        os.remove(filename)
        
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាកើតឡើង៖ {e}")

# Flask integration for Render
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I am alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("Bot is running...")
    bot.infinity_polling()
