# Установка VladShestakov Bot

---

## Требования к системе

Перед установкой убедитесь, что установлены:

- **Python** — среда выполнения (версия по проекту, см. `requirements.txt`)
- **PostgreSQL** — СУБД (порт по умолчанию 5432). В PATH должны быть клиентские утилиты, в том числе `createdb` для создания БД
- **Liquibase CLI** — команда `liquibase` доступна в PATH (накат схемы и тестовых данных). Для работы Liquibase нужны JDK и драйвер JDBC: в каталоге `liquibase/` укажите путь к `lib/postgresql-42.7.7.jar` (см. `liquibase.example.properties`)
- **ОС Windows** — скрипты установки и запуска представлены в виде `.bat`

---

## 1. Создание БД

### Настройка имён БД (при необходимости)

Переменные заданы в `install\db_settings.bat`. По умолчанию:

- `DB_NAME_DEV=vladshestakovbot_dev`

При желании изменить имена — отредактировать `install\db_settings.bat`

### Создание БД (DEV)

```batch
install\create_db_dev.bat
```

Скрипт создаёт базу данных с именем `%DB_NAME_DEV%` от пользователя `postgres`. При успехе в консоли — сообщение «База данных создана».

---

## 2. Создание структуры БД (таблицы)

### Настройка Liquibase

Создать копию файлов настройки из .example в каталоге `liquibase/`:

- `liquibase.example.properties` → `liquibase.properties`

В `liquibase.properties` задать:

- `url` — например `jdbc:postgresql://localhost:5432/vladshestakovbot_dev`
- `username` — пользователь БД
- `password` — пароль

### Создание таблиц

```batch
liquibase\liquibase_run_create_tabs.bat
```

Выполняется накат changelog `ChangeLogs/db.changelog-DEV-100-command-tab.xml`: создаётся таблица `commands`. При успехе в логе — сообщение об успешном выполнении `update`.

---

## 3. Загрузка тестовых данных

```batch
liquibase\liquibase_run_testdata.bat
```

Накатывается changelog `ChangeLogs/db.changelog-DEV-110-test-data.xml`: в таблицу `commands` добавляются примеры команд (version, homelib, weather и т.п.). Ожидаемый вывод — успешный `Liquibase: Update has been successful`.

Проверка в БД:

```sql

select c.id , c.command , c.command_hint , c.message_head , c.active , c.ord , c.message_text , c.image_link , c.image2_link
  from COMMANDS c;
```

```
/*
|command|command_hint       |message_head     |active|ord  |message_text                  |image_link|
|-------|-------------------|-----------------|------|-----|------------------------------|----------|
|homelib|Домашняя библиотека|                 |1     |580  |                              |          |
|weather|Данные о погоде    |Данные о погоде: |1     |610  |/weather_today - Погода на...г|          |
|version|Версия бота        |                 |1     |9 999|                              |          |
 */
```

---

## 4. Настройка бота

Создать рабочую копию в корне проекта:

- `.env.example` → `.env`

В `.env` заполнить:

- `DATABASE_URL` или `DATABASE_URL_TEST` — строка подключения к созданной БД (например, для DEV — к `vladshestakovbot_dev`)
- `API_TOKEN` или `API_TOKEN_TEST` — токен бота от @BotFather
- при необходимости `API_HOMEPATH` / `API_HOMEPATH_TEST` — путь до API Homelib и другие переменные (см. `.env.example` и `params.py`)

Файл `.env` не должен попадать в репозиторий (должен быть в `.gitignore`).

---

## 5. Запуск

### 5.1. Среда выполнения Python и зависимости

Необходимо один раз создать среду выполнения Python (виртуальное окружение) и установить зависимости. Для этого в корне проекта выполните:

```batch
install.bat
```

Скрипт создаёт каталог `.venv`, активирует виртуальное окружение и устанавливает пакеты из `requirements.txt`. Перед первым запуском бота также должен быть настроен файл `.env` (см. п. 4).

### 5.2. Запуск бота локально

Скрипт активирует виртуальное окружение, стартует бота.

```batch
start_server.bat
```

Остановка: **Ctrl+C**.

---

## 6. Проверка

В Telegram откройте бота и проверьте команды:

- `/start`, `/help` — приветствие и справка
- команды из тестовых данных (например, `version`, `homelib`, `weather`) — в соответствии с таблицей `commands`

---

См. также: [README.md](README.md) — назначение проекта, структура, краткая последовательность.
