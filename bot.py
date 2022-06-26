import telebot

import random

import speech_recognition as sr
import subprocess

import gtts


r = sr.Recognizer()


def convert_to_wav(file, name):
    process = subprocess.run([ 'C:\\ffmpeg\\bin\\ffmpeg.exe', '-i', file, name ])
    return process


def convert_to_text(file):
    with sr.AudioFile(file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="ru-RU")

    return text


def convert_text_to_voice(text, lang):
    t1 = gtts.gTTS(text, lang=lang)
    mp3name = f"{random.randint(1, 1000000000)}.mp3"
    t1.save(mp3name)
    return mp3name


bot = telebot.TeleBot("TOKEN", parse_mode=None)


@bot.message_handler(commands=[ 'start' ])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.reply_to(message, f"Привет, {message.from_user.first_name} {message.from_user.last_name}!\nЧтобы "
                          f"конвертировать текст в mp3 просто напиши какой нибудь текст и он сразу конвертируется.\n "
                          f"А для того чтобы войс в текст то скиньте войс сюда")


@bot.message_handler(commands=[ 'help' ])
def help(message):
    sti = open('static/help.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.reply_to(message, "Этот бот создан @AmirBaurzhanov. \nОн создан для конвертирования голосовых в текст и наоборот.")


@bot.message_handler(func=lambda m: True)
def chat(message):
    file = convert_text_to_voice(message.text, "ru")
    files = open(file, 'rb')
    bot.send_audio(message.chat.id, files)


@bot.message_handler(content_types=["voice"])
def convert(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    if new_file:
        name = f"{random.randint(1, 1000000000000)}.wav"
        f = convert_to_wav("new_file.ogg", name)
        if f:
            text = convert_to_text(name)
            bot.reply_to(message, text)


bot.infinity_polling()
