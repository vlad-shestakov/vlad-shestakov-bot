rem Выкачать состояние БД из удаленного сервера на локальный PostgreeSQL

rem 1.Установить параметры в консоли
SET PGUSER=postgres
SET PGPASSWORD=1234567

rem 2.Выкачать
heroku pg:pull DATABASE_URL mylocaldb -a vlad-shestakov-bot
