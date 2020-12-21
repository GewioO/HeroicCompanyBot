# -*- coding: utf-8 -*-
import config, telebot, texts, re
from telebot import types

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, texts.textsStorage['start'])

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, texts.textsStorage['help'])

@bot.message_handler(commands=['write_for'])
def write_characters(message):
    level_number = message.text.replace('/write_for', "")
    bot.send_message(message.chat.id, level_number)

if __name__ == '__main__':
    bot.infinity_polling(True)