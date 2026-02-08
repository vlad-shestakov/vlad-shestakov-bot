@echo off 
@chcp 65001 > nul

@rem Меняем директорию на папку с исполняемым файлом
@cd /d %~dp0
call "%~dp0db_settings.bat"

set MIGRATE_FILE=backup-migrate-20250715-010.sql

@echo Миграция БД из файла - %MIGRATE_FILE%
psql -U postgres %DB_NAME% < %MIGRATE_FILE%

@echo Миграция БД выполнена
pause
