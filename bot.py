# -*- coding: utf-8 -*-
import config, telebot, texts, urllib, os
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
  if message.reply_to_message != None:
    i = 0
    while i < len(recording):
      if recording[i] == str(message.reply_to_message.message_id):
        level_number = message.reply_to_message.text.replace('/write_for', "").strip()
        if level_number:
          document_id = message.photo[0].file_id
          file_info = bot.get_file(document_id)
          urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{config.token}/{file_info.file_path}', file_info.file_path)
          result = postgresql.db_write_image(level_number,file_info.file_path)
          if result:
            bot.send_message(message.chat.id, texts.textsStorage['recorded'])
          else:
            bot.send_message(message.chat.id, texts.textsStorage['error'])
        else:
          bot.send_message(message.chat.id, texts.textsStorage['error'])
      
      i += 1

@bot.message_handler(commands=['level'])
def level_result(message):
  level_number = message.text.replace('/level', "").strip()
  if level_number:
    count = level_number.find("all")
    if count != -1:
      count = level_number[count:len(level_number)]
      level_number = level_number.replace(' all', "")
    else:
      level_number = digit_check(level_number)

    images, ids = postgresql.db_find_photo(level_number, count)
    if images:
      for i in range (0, len(images)):
        bot.send_message(message.from_user.id, texts.textsStorage['level_id'] + ids[i])
        bot.send_photo(message.from_user.id, photo=open(images[i], 'rb'))
    else:
      bot.send_message(message.chat.id, texts.textsStorage['absent_image'])
  else:
    bot.send_message(message.chat.id, texts.textsStorage['error'])

@bot.message_handler(commands=['delete'])
def delete_deck(message):
  ids = message.text.replace('/delete', "").strip()
  ids = ids.split()
  images = []
  
  images, delete_is_need = postgresql.db_delete_photo(ids)

  for i in range(0, len(images)):
    try:
      if postgresql.db_check_path(images[i]):
        os.remove(images[i])
    except(FileNotFoundError):
      break
    
  if delete_is_need:
    bot.send_message(message.chat.id, texts.textsStorage['delete'])
  else:
    bot.send_message(message.chat.id, texts.textsStorage['delete_error'])
  
def digit_check(string):
  if string.isdigit():
    return string
  else:
    num = ""
    for char in string:
      if char.isdigit():
        num = num + char
    
    return num

if __name__ == '__main__':
  bot.infinity_polling(True)