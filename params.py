
# ----------------------------------------------------------
# ИНИЦИАЛИЗАЦИЯ

import os
from dotenv import load_dotenv

load_dotenv()

# Типы стенда
STAND_TYPE_TEST = 'test'
STAND_TYPE_PROD = 'prod'
STAND_TYPE      = STAND_TYPE_PROD

# Режим отладки
IS_DEBUG        = False

# Параметры приложения
APP_NAME        = 'VladShestakovBot Server version' # Название программы
APP_VERSION     = '1.0.7 (08.02.2026)'              # Версия программы
IMAGES_PATH     = 'res\\images\\'                   # Путь до папки с картинками
# Токен телеграм бота
if STAND_TYPE == STAND_TYPE_PROD:
    API_TOKEN = os.getenv("API_TOKEN")
    LOG_FILENAME    = 'vlad-shestakov-bot.log'          # Имя файла лога
else:
    API_TOKEN = os.getenv("API_TOKEN_TEST")
    LOG_FILENAME    = 'vlad-shestakov-test-bot.log'          # Имя файла лога


if STAND_TYPE == STAND_TYPE_TEST:
    IS_DEBUG = True