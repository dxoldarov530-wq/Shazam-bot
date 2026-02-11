import telebot
import yt_dlp
import os
from telebot import types

# Sizning bot tokeningiz
TOKEN = '8251259734:AAFF3UQe6vlzjPBGACnQfUdrnGh2gXvGkPM'
bot = telebot.TeleBot(TOKEN)

def download_music(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1:',
        'outtmpl': 'music.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        title = info['entries'][0]['title']
        return title

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Musiqa izlash 🔍")
    bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}! Musiqa nomini yozing:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if message.text == "Musiqa izlash 🔍":
        bot.send_message(message.chat.id, "Qaysi qo'shiqni qidiramiz? Nomini yozing:")
    else:
        status_msg = bot.send_message(message.chat.id, "Qidirilmoqda... ⏳")
        try:
            title = download_music(message.text)
            with open('music.mp3', 'rb') as audio:
                bot.send_audio(message.chat.id, audio, caption=f"✅ Topildi: {title}")
            os.remove('music.mp3')
            bot.delete_message(message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text("Xato yuz berdi yoki musiqa topilmadi. ❌", message.chat.id, status_msg.message_id)

# Botni uzluksiz ishlashi uchun
if __name__ == "__main__":
    print("Bot serverda ishga tushdi...")
    bot.infinity_polling()
