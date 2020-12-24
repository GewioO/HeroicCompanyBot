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
            bot.send_message(message.chat.id, "Your deck is recorded")
          else:
            bot.send_message(message.chat.id, "Something wrong")
        else:
          bot.send_message(message.chat.id, "Something wrong")
      
      i += 1

@bot.message_handler(commands=['level'])
def level_result(message):
  ##bot.send_photo(message.from_user.id, photo=open('photos/file_5.jpg', 'rb'))
  level_number = message.text.replace('/level', "").strip()
  if level_number:
    count = level_number.find("all")
    if count != -1:
      count = level_number[count:len(level_number)]
      level_number = level_number.replace(' all', "")
    else:
      level_number = digit_check(level_number)

    images = postgresql.db_find_photo(level_number, count)
    if images:
      for i in range (0, len(images)):
        bot.send_photo(message.from_user.id, photo=open(images[i], 'rb'))
        print("image " + str(i) + " = " + str(images[i]))
    else:
      bot.send_message(message.chat.id, "You don't have any images for this level")
  else:
    bot.send_message(message.chat.id, "Something wrong")
  print(str(message.from_user.id))

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