# vlad-shestakov-bot-priv

Тестовый Telegram-бот [VladShestakovBot](https://web.telegram.org/z/#1722864364). Стек: Python, PostgreSQL, Liquibase. Установка и запуск — [install.md](install.md).

### Назначение

Бот написан на Python, использует БД PostgreSQL. Команды обрабатываются с учётом данных из таблицы `commands`; часть функций (например, каталог книг) завязана на внешний API (Homelib). Подробная пошаговая установка и инициализация БД — в [install.md](install.md).

### Структура проекта

```
vlad-shestakov-bot.py, params.py, requirements.txt, .env.example, README.md, install.md
install.bat, act.bat, start_server.bat, ...   — скрипты запуска и окружения

install/          — скрипты БД: create_db_dev.bat, db_settings.bat, бэкапы и восстановление
liquibase/        — миграции схемы БД и тестовых данных, example-конфиги, bat-скрипты наката
res/              — ресурсы (изображения и т.п.)
modules/          — дополнительные модули
```

### Команды бота

- **/help**, **/start** — справка и приветствие
- Остальные команды задаются в таблице `commands` (см. тестовые данные в [install.md](install.md))
- **/homelib** - Домашняя библиотека (Требуется API проекта [Домашняя библиотека. Микросервис GitHub](https://github.com/vlad-shestakov/homelibrary-ms))
- **/weather** - Данные о погоде (Требуется Модуль solar-times - \modules\solar-times)
- **/version** - Версия бота

/homelib - Домашняя библиотека
/weather - Данные о погоде
/version - Версия бота

### Требования

Python, PostgreSQL (в PATH — клиентские утилиты, в т.ч. `createdb`), Liquibase CLI, ОС Windows для .bat-скриптов. Подробнее — [install.md](install.md).

## Установка

Получить токен бота у [@BotFather](https://t.me/BotFather), записать его. Создать среду выполнения Python и установить зависимости: `install.bat`. Далее — пошаговая инструкция по БД, `.env` и запуску в [install.md](install.md).
