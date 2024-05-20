@echo off
rem S'assurer que la version standard de Python est installée

set "PYTHON_ENV=C:\Users\EXEIO\AppData\Local\Programs\Python\Python311"
set "PROJECT_WORKSPACE=C:\path\to\project"
set "VENV_PATH=%PROJECT_WORKSPACE%\env_project"

rem Créer l'environnement virtuel si ce n'est pas déjà fait
if not exist "%VENV_PATH%\Scripts\python.exe" (
    "%PYTHON_ENV%\python.exe" -m venv "%VENV_PATH%"
)

rem Installer les packages nécessaires
"%VENV_PATH%\Scripts\python.exe" -m pip install -r "%PROJECT_WORKSPACE%\requirements.txt"

rem Exécuter le script Python
"%VENV_PATH%\Scripts\python.exe" "%PROJECT_WORKSPACE%\main.py"
