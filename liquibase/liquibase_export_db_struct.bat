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


liquibase^
 --defaults-file=liquibase.properties^
 --changeLogFile=diffChangeLogs\db.changelog-export-struct-%DT%.xml^
 generateChangeLog

@rem  status
@rem OPERATIONS: 
@rem   	status 			- test run only
@rem   	generateChangeLog       - Export all structure DB
@rem   	update	                - update operation 
@rem    update-sql		- update operation with SQL commands
