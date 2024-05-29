@echo off
SETLOCAL

:: Variables
SET "PGSQL_PATH=C:\Program Files\PostgreSQL\16\bin"
SET "SQL_SCRIPT_PATH=C:\_project\M1_project\data_project-end-to-end-solo-\setup_postgresql.sql"
SET "DB_USER=postgres"
SET "DB_NAME=datawarehouse"
SET "DB_PASSWORD=root"

:: Ajouter PostgreSQL au PATH
echo Adding PostgreSQL to PATH...
SETX PATH "%PATH%;%PGSQL_PATH%"
SET "PATH=%PATH%;%PGSQL_PATH%"

:: Exécuter le script SQL
echo Executing SQL script...
psql -U %DB_USER% -h localhost -f "%SQL_SCRIPT_PATH%"

:: Fin
echo Script execution completed.
pause
ENDLOCAL
exit
