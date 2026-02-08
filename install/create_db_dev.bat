@echo off 
@chcp 65001 > nul

@rem Меняем директорию на папку с исполняемым файлом
@cd /d %~dp0
call "%~dp0db_settings.bat"

@echo Создает БД PostgreSQL - %DB_NAME_DEV% / User - postgres
createdb -U postgres %DB_NAME_DEV%
@rem createdb -h YOUR_HOST -p YOUR_PORT -U YOUR_USER YOUR_DATABASE

@echo База данных создана
pause
