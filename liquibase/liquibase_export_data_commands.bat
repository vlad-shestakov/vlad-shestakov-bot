@rem Execute LIQUIBASE command
@rem    get file <changeLogFile> 
@rem    db type and path in <url>
@rem    jdbc driver name in <classpath>
@rem    run commant - status | update | generateChangeLog
@rem 
@rem    other patams get from - liquibase.properties
@rem 

@rem Time in format: 2025-03-24-030913
@set DT=%DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2%-%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
@set DT=%DT: =0%

@set TABLE_NAME=commands
@set CHANGELOG_FILE_NAME=db.changelog-export-%TABLE_NAME%-data-%DT%.xml


@echo Export table data - %TABLE_NAME%
liquibase^
 --defaults-file=liquibase.properties^
 --changeLogFile=diffChangeLogs\%CHANGELOG_FILE_NAME%^
 --diffTypes=data^
 --includeObjects=table:%TABLE_NAME%^
 --overwrite-output-file=true^
 generateChangeLog

@rem --database-changelog-table-name: To change the name of the DATABASECHANGELOG table.
@rem --database-changelog-lock-table-name: To change the name of the DATABASECHANGELOGLOCK table.

@rem --log-file=liquibase.log
@rem   https://docs.liquibase.com/parameters/log-file.html

@rem liquibase.outputFile
@rem   https://docs.liquibase.com/parameters/output-file.html

@rem  status
@rem OPERATIONS: 
@rem   	status 			- test run only
@rem   	generateChangeLog       - Export all structure DB
@rem   	update	                - update operation 
@rem    update-sql		- update operation with SQL commands
