@echo off 
@chcp 65001 > nul

@rem Меняем директорию на папку с исполняемым файлом
@cd /d %~dp0


@rem Execute LIQUIBASE command
@rem    get file <changeLogFile> 
@rem    db type and path in <url>
@rem    jdbc driver name in <classpath>
@rem    run commant - status | update | generateChangeLog
@rem 
@rem    other patams get from - liquibase.properties
@rem 
liquibase^
 --changeLogFile=db.changelog-master.xml^
 --defaults-file=liquibase-prod.properties^
 update

@rem  status
@rem OPERATIONS: 
@rem   	status 			- test run only
@rem   	generateChangeLog       -
@rem   	update	                - update operation 
@rem    update-sql		- update operation with SQL commands
