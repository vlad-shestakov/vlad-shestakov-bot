@echo off 
@chcp 65001 > nul

@rem Меняем директорию на папку с исполняемым файлом
@cd /d %~dp0


@rem Execute LIQUIBASE command - тестовые данные (пары книг), идемпотентно
@rem    other params get from - liquibase.properties
@rem 
liquibase^
 --changeLogFile=ChangeLogs/db.changelog-DEV-100-command-tab.xml^
 --defaults-file=liquibase.properties^
 update

@rem  status
@rem OPERATIONS: 
@rem   	status 			- test run only
@rem   	update	                - update operation 
@rem    update-sql		- update operation with SQL commands
