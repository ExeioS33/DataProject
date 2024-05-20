# Projet de Collecte et d'Insertion de Données Financières

Ce projet permet de récupérer des données historiques des actions du CAC 40 à l'aide de l'API `yfinance`, de les sauvegarder dans des fichiers CSV, puis d'insérer ces données dans une base de données PostgreSQL en continu afin de pouvoir entrainer des modèles de machine learning.

## Prérequis

1. **Python 3.11** (ou version compatible) : Assurez-vous que Python est installé. [Télécharger Python](https://www.python.org/downloads/)
2. **PostgreSQL** : Assurez-vous que PostgreSQL est installé et en cours d'exécution. [Télécharger PostgreSQL](https://www.postgresql.org/download/)

## Installation et Exécution

1. **Téléchargement du Projet**

   Téléchargez et extrayez le projet dans le répertoire de votre choix.

2. **Configuration de la Base de Données PostgreSQL**

    Lire `setup.md`

3. **Configuration de l'Environnement de Développement**

    Un script batch est fourni pour automatiser le processus de configuration de l'environnement de développement. Voici les étapes pour l'utiliser :

    ### Script Batch (`deploy_and_run.bat`)

    ```batch
    @echo off
    rem S'assurer que la version standard de Python est installée

    set "PYTHON_ENV=C:\Users\EXEIO\AppData\Local\Programs\Python\Python311"
    set "PROJECT_WORKSPACE=C:\path\to\project"
    set "VENV_PATH=%PROJECT_WORKSPACE%\my_env"

    rem Créer l'environnement virtuel si ce n'est pas déjà fait
    if not exist "%VENV_PATH%\Scripts\python.exe" (
        "%PYTHON_ENV%\python.exe" -m venv "%VENV_PATH%"
    )

    rem Installer les packages nécessaires
    "%VENV_PATH%\Scripts\python.exe" -m pip install -r "%PROJECT_WORKSPACE%\requirements.txt"

    rem Exécuter le script Python
    "%VENV_PATH%\Scripts\python.exe" "%PROJECT_WORKSPACE%\main.py"
    ```

    ### Exécution du Script Batch

    Pour exécuter le script batch, suivez ces étapes :

    - Ouvrez une fenêtre de commande (cmd).
    - Naviguez jusqu'au répertoire où le script batch est situé.
    - Exécutez la commande suivante ou simplement double-cliquez sur le fichier dans votre explorateur de fichiers:
    
      ```sh
      deploy_and_run.bat
      ```

    ### Détails du Script Batch

    Le fichier batch fourni (`deploy_and_run.bat`) est conçu pour automatiser le processus de configuration de l'environnement de développement. Voici un résumé de sa logique :

    1. **Définition des variables d'environnement** :
       - `PYTHON_ENV` : Chemin de l'installation standard de Python.
       - `PROJECT_WORKSPACE` : Chemin du répertoire du projet.
       - `VENV_PATH` : Chemin où l'environnement virtuel sera créé.

    2. **Création de l'environnement virtuel** :
       - Si l'environnement virtuel n'existe pas déjà, il est créé avec la commande `python -m venv`.

    3. **Installation des dépendances** :
       - Les packages nécessaires sont installés à partir du fichier `requirements.txt` à l'aide de `pip install`.

    4. **Exécution du script principal** :
       - Le script principal (`main.py`) est exécuté en utilisant l'interpréteur Python de l'environnement virtuel.

## Tests

Pour s'assurer que les différentes parties du projet fonctionnent correctement, des tests unitaires ont été définis. Les tests sont organisés dans un répertoire séparé à la racine du projet.

### Structure des Tests

L'arborescence des fichiers de tests est la suivante :


   ```my_project/
   ├── financial_package/
   │ ├── init.py
   │ ├── cac40_historical_data.py
   │ ├── insert_into_postgres.py
   ├── tests/
   │ ├── init.py
   │ ├── test_cac40_historical_data.py
   │ ├── test_insert_into_postgres.py
   ├── config.py
   ├── main.py
   ├── requirements.txt
   └── deploy_and_run.bat
   ```


### Exécution des Tests

Pour exécuter les tests, utilisez la commande suivante depuis la racine du projet :

```sh
"C:\chemin\vers\env_virtuel\Scripts\python.exe" -m unittest discover -s tests
```
