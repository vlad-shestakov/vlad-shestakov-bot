#!/usr/bin/python
from logging import NullHandler


# ----------------------------------------------------------
import params as p # Параметры приложения
import telebot
import logging
from io import BytesIO
from telebot.types import InputMediaPhoto
import homelib_api
import solar_times_client
import time

from bd1 import BD1
logging.basicConfig(filename=p.LOG_FILENAME, level=logging.INFO
                    ,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ----------------------------------------------------------
def show_invite_message():
    logger.info(f"{p.APP_NAME} {p.APP_VERSION}")
    logger.info(f"STAND_TYPE - {p.STAND_TYPE}")
    print(f"{p.APP_NAME} {p.APP_VERSION}")
    print(f"STAND_TYPE - {p.STAND_TYPE}")
    print(f"LOG_FILENAME - {p.LOG_FILENAME}")
    if p.IS_DEBUG:
        print(f"IS_DEBUG   - {p.IS_DEBUG}")
    db_stat_msg = BD1.get_db_status()
    print(db_stat_msg)
    logger.info(db_stat_msg)
    print("Quit the server with CTRL-BREAK")

# ----------------------------------------------------------
# Основной код приложения

# Вывод сообщений о запуске в консоль
show_invite_message()

bot = telebot.TeleBot(p.API_TOKEN)

# ----------------------------------------------------------
def get_version():
    # Возвращает версию приложения
    return f'Версия приложения - {p.APP_VERSION}'

# ----------------------------------------------------------
def get_log_msg(message, oper_name):
    # Возвращает сообщение для логирования
    return f"[{oper_name}] User:{message.from_user.username}({message.from_user.id}) Command: {message.text}"

# ----------------------------------------------------------
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    logger.info(get_log_msg(message, "START  "))
    msg = f'\nСписок команд:'
    try:
        command_list = BD1.command_list()
        msg = msg + f'{command_list}'
    except Exception as e:
        logger.error(f"Ошибка 'send_welcome': {e}")
    bot.reply_to(message, msg)

# ----------------------------------------------------------
# Тестовая функция
def test_function():
    return """Данные о погоде: 
/noon - Когда полдень
/sun_today - Данные солнца на сегодня
/sun_graph - График солнечной активности"""

# ----------------------------------------------------------
# Handle '/test' - тестовая команда
@bot.message_handler(commands=['test'])
def send_welcome(message):
    logger.info(get_log_msg(message, "TEST  "))
    msg = f'\nTest:'
    try:
        test_function_res = test_function()
        msg = msg + f' {test_function_res}'
    except Exception as e:
        logger.error(f"Ошибка 'test_function': {e}")
    bot.reply_to(message, msg)


# ----------------------------------------------------------
# Handle '/noon' - Когда полдень
@bot.message_handler(commands=['noon'])
def send_noon(message):
    logger.info(get_log_msg(message, "NOON  "))
    msg = "Ошибка команды"
    try:
        msg = solar_times_client.get_solar_noon(logger_var=logger)
    except Exception as e:
        logger.error(f"Ошибка 'send_noon': {e}")
    msg = f'{msg}\nДанные о погоде /weather'
    bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/sun_today' - Данные солнца на сегодня
@bot.message_handler(commands=['sun_today'])
def send_solar_times(message):
    logger.info(get_log_msg(message, "SONDAY"))
    msg = "Ошибка команды"
    try:
        msg = solar_times_client.get_solar_times_text(logger_var=logger)
    except Exception as e:
        logger.error(f"Ошибка 'send_solar_times': {e}")
    msg = f'{msg}\nДанные о погоде /weather'
    bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/weather_today' - Погода на сегодня
@bot.message_handler(commands=['weather_today'])
def send_weather_today(message):
    logger.info(get_log_msg(message, "WEATH "))
    msg = "Ошибка команды"
    try:
        msg = solar_times_client.get_weather_text(logger_var=logger, city="spb", content_type="html")
    except Exception as e:
        logger.error(f"Ошибка 'send_weather_today': {e}")
    msg = f'{msg}\nДанные о погоде /weather'
    # Telegram HTML mode does not support <br>; normalize to newlines
    msg = msg.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    try:
        bot.reply_to(message, msg, parse_mode="HTML")
    except Exception as e:
        logger.error("send_weather_today reply error: %s", e)
        truncated_msg = msg[:500] + "..." if len(msg) > 500 else msg
        logger.error("Текст сообщения (обрезано): %s", truncated_msg)
        bot.reply_to(message, msg, parse_mode=None)

# ----------------------------------------------------------
# Handle '/sun_graph' - График солнечной активности
@bot.message_handler(commands=['sun_graph'])
def send_solar_plot(message):
    logger.info(get_log_msg(message, "PLOT  "))
    try:
        image_bytes, msg = solar_times_client.get_solar_plot(logger_var=logger)
        if image_bytes is not None:
            image_msg = f'{msg}\nДанные о погоде /weather'
            bot.send_photo(
                message.chat.id,
                BytesIO(image_bytes),
                caption=image_msg,
            )
        else:
            msg = f'{msg}\nДанные о погоде /weather'
            bot.reply_to(message, msg)
    except Exception as e:
        logger.error(f"Ошибка 'send_solar_plot': {e}")
        msg = "Произошла ошибка обработки: " + str(e)
        msg = f'{msg}\nДанные о погоде /weather'
        bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/homelib' - Корневая страница библиотеки
@bot.message_handler(commands=[homelib_api.HOMELIB_MAIN_COMMAND])
def send_homelib_main(message):
    logger.info(get_log_msg(message, "COMMAND"))
    msg = homelib_api.get_msg_homelib_main()
    image_link = f'{p.IMAGES_PATH}{homelib_api.HOMELIB_MAIN_IMAGE}'
    if image_link:
        image = open(image_link, 'rb')
        bot.send_photo(message.chat.id, image, caption=msg, parse_mode='HTML')
    else:
        bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/books' - Cтраница список книг
@bot.message_handler(commands=[homelib_api.LIST_BOOKS_COMMAND])
def send_homelib_books_list(message):
    logger.info(get_log_msg(message, "COMMAND"))
    msg = homelib_api.get_msg_books_list()
    bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/recentbooks' - Cтраница Последние поступления
@bot.message_handler(commands=[homelib_api.LAST_BOOKS_COMMAND])
def send_homelib_recent(message):
    logger.info(get_log_msg(message, "COMMAND"))
    msg = homelib_api.get_msg_books_recent_list()
    bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/categories' - Cтраница Последние поступления
@bot.message_handler(commands=[homelib_api.CATS_BOOKS_COMMAND])
def send_homelib_categories(message):
    logger.info(get_log_msg(message, "COMMAND"))
    msg = homelib_api.get_msg_cats_list()
    bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/booksearch' - Поиск по названию, автору
@bot.message_handler(commands=[homelib_api.SEARCH_BOOKS_COMMAND])
def send_homelib_booksearch(message):
    logger.info(get_log_msg(message, "COMMAND"))
    msg = homelib_api.get_msg_homelib_booksearch()
    bot.send_message(chat_id=message.chat.id, text = msg)
    bot.register_next_step_handler(message, send_homelib_booksearch_res) # Следующий обработчик для обработки ввода пользователя

# ----------------------------------------------------------
# Обработка результата поиска по названию, автору
@bot.message_handler(commands=[homelib_api.SEARCH_BOOKS_COMMAND])
def send_homelib_booksearch_res(message):
    logger.info(get_log_msg(message, "COMMAND"))
    search_text = message.text.strip()
    res, err_msg = homelib_api.check_msg_homelib_booksearch(search_text)
    if res > 0:
        bot.reply_to(message, err_msg)
    else:
        msg = homelib_api.get_msg_search_books_by_title_autor(search_text)
        bot.reply_to(message, msg)

# ----------------------------------------------------------
# Handle '/version'
@bot.message_handler(commands=['version'])
def send_ver(message):
    logger.info(get_log_msg(message, "VERSION"))
    bot.reply_to(message, get_version())

"""
    logger.info(get_log_msg(message, "COMMAND"))
    msg = homelib_api.get_msg_homelib_main()
    image_link = f'{p.IMAGES_PATH}{homelib_api.HOMELIB_MAIN_IMAGE}'
    if image_link:
        image = open(image_link, 'rb')
        bot.send_photo(message.chat.id, image, caption=msg, parse_mode='HTML')
    else:
        bot.reply_to(message, msg)"""

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    logger.info(get_log_msg(message, "COMMAND"))
    # Найдем команду в БД
    try:
        cmd = message.text.lower()
        cmd_raw = message.text
        result = BD1.get_command(cmd)
        # print(f'result - {result}')
        book_id = homelib_api.check_command_book_id(cmd_raw) # получаем book_id из ссылки
        lib_page_id = homelib_api.check_command_lib_page_id(cmd_raw) # получаем page_id из ссылки
        cat_alias = homelib_api.check_command_cat_name(cmd_raw) # получаем cat_name из ссылки
        if book_id is not None and book_id > 0:
            msg, img_cover = homelib_api.get_msg_book_by_id(book_id)
            if img_cover is not None:
                # Отправляем обложку и карточку книги пользователю
                bot.send_photo(chat_id=message.chat.id, photo=img_cover, caption=msg)
            else:
                # Отправляем только карточку
                bot.reply_to(message, msg)
        elif lib_page_id is not None and lib_page_id >= 0:
            msg = homelib_api.get_msg_books_list(lib_page_id)
            bot.reply_to(message, msg)
        elif cat_alias is not None and len(cat_alias) > 0:
            msg = homelib_api.get_msg_books_by_cat_list(cat_alias)
            bot.reply_to(message, msg)
        elif result is not None:
            # print("result is not None")
            # Если команда из Базы данных
            command_header, message_text, image_link, image2_link = result
            # Готовим сообщение
            if command_header is not None:
                pass
            msg = f"<b>{command_header}</b>\n\n"
            msg = msg + f"{message_text}"
            # Отправляем, добавляем изображения, если они указаны
            if image2_link:
                media = [
                    InputMediaPhoto(media=open(image_link, 'rb'), caption=msg, parse_mode='HTML'),
                    InputMediaPhoto(media=open(image2_link, 'rb'))
                ]
                bot.send_media_group(chat_id=message.chat.id, media=media)
            elif image_link:
                try:
                    image = open(image_link, 'rb')
                    bot.send_photo(message.chat.id, image, caption=msg, parse_mode='HTML')
                except Exception as e:
                    logger.error(f"Ошибка отправки фото (image_link={image_link}): {e}", exc_info=True)
                    bot.send_message(message.from_user.id, msg, parse_mode='HTML')
            else:
                bot.send_message(message.from_user.id, msg, parse_mode='HTML')
        else:
            # Не нашли подходящую команду
            bot.send_message(message.from_user.id, 'Не понимаю, что это значит. Используйте /help')
    except Exception as e:
        logger.error(f"Ошибка 'get_text_messages': {e}",exc_info=True)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(e, exc_info=True)
        time.sleep(15)
        logger.info("Pooling restart")