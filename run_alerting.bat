@echo off
REM Ask the user for the virtual environment path
set "PROJECT_VENV_PATH=C:\_project\M1_project\data_project-end-to-end-solo-\my_env"

REM Activate the virtual environment
call "%PROJECT_VENV_PATH%\Scripts\activate"

REM Run the alerting.py script using the Python executable from the virtual environment
"%PROJECT_VENV_PATH%\Scripts\python.exe" "%~dp0alerting.py"

REM Deactivate the virtual environment
call "%PROJECT_VENV_PATH%\Scripts\deactivate"
