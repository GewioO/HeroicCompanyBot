# -*- coding: utf-8 -*-
import config, telebot, texts, re, urllib
from lib import directory_help, postgresql
from telebot import types

bot       = telebot.TeleBot(config.token)
recording = []

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, texts.textsStorage['start'])

@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, texts.textsStorage['help'])

@bot.message_handler(commands=['write_for'])
def write_characters(message):
  global recording
  recording.append(str(message.message_id))
  text_send = message.text.replace('/write_for', "")
  bot.send_message(message.chat.id, texts.textsStorage['write_for'] + text_send)

@bot.message_handler(content_types=['photo'])
def photoProcessing(message):
  global recording
  bot.send_message(message.chat.id, "PHOTO")
  if message.reply_to_message != None:
    i = 0
    while i < len(recording):
      if recording[i] == str(message.reply_to_message.message_id):
        level_number = message.reply_to_message.text.replace('/write_for', "")
  
        document_id = message.photo[0].file_id
        file_info = bot.get_file(document_id)
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{config.token}/{file_info.file_path}', file_info.file_path)
        postgresql.db_write_image(level_number,file_info.file_path)
        bot.send_message(message.chat.id, "!!!  " + file_info.file_path)
      
      i += 1

if __name__ == '__main__':
  bot.infinity_polling(True)