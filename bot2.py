#import config
#import logging
#import asyncio
from bd1 import BD1

#from aiogram import Bot, Dispatcher, executor, types

#logging.basicConfig(level=logging.INFO)

'''
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def subscribe(message: types.Message):
    await message.reply("Прииивет ")
    await message.reply(BD1.ss())


if __name__ == '__main__':
    executor.start_polling(dp)
    
'''

#BD1.ss()
print(BD1.ss())