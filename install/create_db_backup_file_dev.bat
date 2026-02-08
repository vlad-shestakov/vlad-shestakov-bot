@echo off 
@chcp 65001 > nul

@rem Меняем директорию на папку с исполняемым файлом
@cd /d %~dp0
call "%~dp0db_settings.bat"

@echo Create backup file from PostgreSQL DB - %DB_NAME_DEV%
pg_dump -U postgres %DB_NAME_DEV% > %BACKUP_FILE_DEV%

@echo Резервная копия создана - %BACKUP_FILE_DEV%

pause