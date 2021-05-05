#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import os
from bd1 import BD1


# На сервере Heroku установить переменную окружения
# heroku config:set BOT_TOKEN=<YOUR_TOKEN> -a <YOUR_APP_NAME>

API_TOKEN = os.environ['BOT_TOKEN']
VERSION = '1.0.0.12'

bot = telebot.TeleBot(API_TOKEN)

def get_version():
    """Возвращает версию приложения"""
    return (f'Версия приложения - {VERSION}')

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """Сообщение для /help /start"""
    bot.reply_to(message, \
                 f'\nПривет,  {message.from_user.first_name}, я бот Владмир.'+\
                 """\n
Я использую команды /start /help /ver 
us - Список пользователей (чтение из БД)
po - Список постов (чтение из БД)
привет - отзыв""")

# Handle '/ver'
@bot.message_handler(commands=['ver'])
def send_ver(message):
    bot.reply_to(message, get_version())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text.lower() == 'us':
        users_list = BD1.users_list()
        bot.reply_to(message, f'\nСписок пользователей:\n{users_list}')
    elif message.text.lower() == 'po':
        po_list = BD1.posts_list()
        bot.reply_to(message, f'\nСписок постов пользователей:\n{po_list}')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит. Используйте /help')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)
# print(BD1.users_list())
