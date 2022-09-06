# vlad-shestakov-bot
Test telegram bot - [VladShestakovBot](https://web.telegram.org/z/#1722864364)

## Как это устроено:
* Бот написан на Python
* Развернут на сервисе - heroku.com
* Обновляется и деплоится автоматически через репозиторий GitHub
* Использует БД PostgreSQL 

## Команды:
* **/help /start**
* **us** - Список пользователей из БД (только чтение)
* **po** - Список постов пользователей из БД (только чтение)
* **привет**

Первоначально использовал инструкцию:
https://tproger.ru/translations/telegram-bot-create-and-deploy/

# Установка
## Настройка бота
* Заказать себе бота на @BotFather
* Назвать его как-нибудь, записать токен авторизации
## Настройка Heroku
* Зарегистрироваться на сервере [heroku.com](heroku.com)
* Скачать командную строку для Heroku ([HerokuCli](https://devcenter.heroku.com/articles/heroku-cli))
* После установки HerocuCLI он должен быть доступен из консоли
* Авторизоваться через консоль
  > heroku login
* Создать модуль-приложение через консоль
  > heroku create vlad-shestakov-bot
* Добавить переменную окружения с вашимм токеном
  > heroku config:set BOT_TOKEN=НВАШ_ТОКЕН -a vlad-shestakov-bot
* В интерфейсе Heroku привязать ваш гит репозиторий
* Выставить автоматический редеплой приложения после коммита репозитория
* Настроить БД в Heroku:
  * [Справка по Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#set-up-postgres-on-windows)
  * Добавить модуль PostrgeSQL в сервис
  > heroku addons:create heroku-postgresql:hobby-dev
  * После создания адрес БД будет записан в переменной среды - DATABASE_URL
  * Подключиться к БД через PSQL
  > heroku pg:psql -a vlad-shestakov-bot
  * Накатить скрипты из папки **setup\createdb.sql**
## Запуск приложения
* Запуская батники в bin 
* Через интерфейс или командой (**_run.bat**) 
  > heroku ps:scale worker=1 -a vlad-shestakov-bot
* Наблюдать за логом командой (**show_log.bat**)
> heroku logs --tail -a vlad-shestakov-bot
