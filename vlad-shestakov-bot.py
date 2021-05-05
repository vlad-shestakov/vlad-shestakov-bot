#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import os
from bd1 import BD1
# print('123')

# На сервере Heroku установить переменную окружения
# heroku config:set BOT_TOKEN=<YOUR_TOKEN> -a <YOUR_APP_NAME>

API_TOKEN = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я бот Владмира Шестакова!\n
Я использую команды start / help / us / привет"""+\
                 f'\nВаше имя - {message.from_user.first_name}')


# Handle '/start' and '/help'
@bot.message_handler(commands=['us'])
def send_welcome(message):
    users_list = BD1.us_list()
    bot.reply_to(message, f'\nСписок пользователей: {users_list}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)
# print(BD1.ss())
