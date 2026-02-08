@echo off 
@chcp 65001 > nul

@rem Меняем директорию на папку с исполняемым файлом
@cd /d %~dp0
call "%~dp0db_settings.bat"

@echo Восстановление БД из резервной копии - %BACKUP_FILE%
psql -U postgres %DB_NAME% < %BACKUP_FILE%

@echo Состояние БД восстановлено
pause
