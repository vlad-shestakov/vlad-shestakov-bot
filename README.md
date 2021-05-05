# vlad-shestakov-bot
Test telegram bot - vlad-shestakov-bot

Команды:
* /help /start
* привет

Как это устроено:
Бот развернут на сервере - heroku.com

Первоначально использовал инструкцию:
https://tproger.ru/translations/telegram-bot-create-and-deploy/

# Установка
* Заказать себе бота на @BotFather
* Назвать его как-нибудь, записать токен авторизации
* Зарегистрироваться на сервере heroku.com
* Скачать командную строку для Heroku (HerokuCli)
  https://devcenter.heroku.com/articles/heroku-cli
* После установки HerocuCLI он должен быть доступен из консоли
* Авторизоваться через консоль
  * heroku login
* Создать приложение через консоль
  У меня это - heroku create vlad-shestakov-bot
* Добавить переменную окружения с вашимм токеном
  * heroku config:set BOT_TOKEN=НВАШ_ТОКЕН -a vlad-shestakov-bot
* В интерфейсе Heroku привязать ваш гит репозиторий
* Выставить автоматический редеплой приложения после коммита репозитория
* Запустить приложение через интерфейс или командой 
  * heroku ps:scale worker=1 -a vlad-shestakov-bot
* Наблюдать за логом командой Смотреть логи
heroku logs --tail

