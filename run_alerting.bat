@echo off
REM Ask the user for the virtual environment path
set "PROJECT_VENV_PATH=C:\Users\Benja\projet_sup_de_vinci\DataProject\env_project"

REM Activate the virtual environment
call "%PROJECT_VENV_PATH%\Scripts\activate"

REM Run the alerting.py script using the Python executable from the virtual environment
"%PROJECT_VENV_PATH%\Scripts\python.exe" "%~dp0alerting.py"

REM Deactivate the virtual environment
call "%PROJECT_VENV_PATH%\Scripts\deactivate"
