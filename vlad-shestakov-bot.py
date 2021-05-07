#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import os
from bd1 import BD1
from telebot import types

# На сервере Heroku установить переменную окружения
# heroku config:set BOT_TOKEN=<YOUR_TOKEN> -a <YOUR_APP_NAME>

API_TOKEN = os.environ['BOT_TOKEN']
VERSION = '1.0.16 (06.05.2021)'

bot = telebot.TeleBot(API_TOKEN)


def get_version():
    """Возвращает версию приложения"""
    return f'Версия приложения - {VERSION}'


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """Сообщение для /help /start"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/ver")
    item2 = types.KeyboardButton("/us")
    item3 = types.KeyboardButton ("/po")
    markup.add(item1, item2, item3)
    bot.reply_to(message,
                 f'\nПривет,  {message.from_user.first_name}, я бот Владимир.' +
                 """\n
Я использую команды /start /help /ver 
/us - Список пользователей (чтение из БД)
/po - Список постов (чтение из БД)
привет - отзыв""", reply_markup=markup)


# Handle '/ver'
@bot.message_handler(commands=['ver'])
def send_ver(message):
    bot.reply_to(message, get_version())


# Handle '/us'
@bot.message_handler(commands=['us'])
def send_ver(message):
    users_list = BD1.users_list()
    bot.reply_to(message, f'\nСписок пользователей:\n{users_list}')


# Handle '/po'
@bot.message_handler(commands=['po'])
def send_ver(message):
    po_list = BD1.posts_list()
    bot.reply_to(message, f'\nСписок постов пользователей:\n{po_list}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит. Используйте /help')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)
# print(BD1.users_list())
