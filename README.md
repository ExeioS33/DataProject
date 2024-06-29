# Projet de Collecte et d'Insertion de Données Financières

Ce projet permet de récupérer des données historiques des actions du CAC 40 à l'aide de l'API `yfinance`, de les sauvegarder dans des fichiers CSV, puis d'insérer ces données dans une base de données PostgreSQL en continu afin de pouvoir entrainer des modèles de machine learning.

## Prérequis

1. **Python 3.11** (ou version compatible) : Assurez-vous que Python est installé. [Télécharger Python](https://www.python.org/downloads/)
2. **PostgreSQL** : Assurez-vous que PostgreSQL est installé et en cours d'exécution. [Télécharger PostgreSQL](https://www.postgresql.org/download/)

## Installation et Exécution

1. **Téléchargement du Projet**

   Téléchargez et extrayez le projet dans le répertoire de votre choix.

2. **Configuration de la Base de Données PostgreSQL**

    Lire [setup.md](https://github.com/ExeioS33/DataProject/blob/main/setup.md)

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
    - Exécutez la commande suivante :
    
      ```sh
      deploy_and_run.bat
      ```

    ### Détails du Script Batch

    Le fichier batch fourni (`deploy_and_run.bat`) est conçu pour automatiser le processus de configuration de l'environnement de développement. Voici un résumé de sa logique :

    1. **Définition des variables d'environnement (qu'il faudra renseigner avec les vrais chemins)** :
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
   │ ├── get_historical_data.py
   │ ├── postgres_utils.py
   │ ├── etl.py
   ├── tests/
   │ ├── init.py
   │ ├── test_cac40_historical_data.py
   │ ├── test_insert_into_postgres.py
   ├── config.py
   ├── main.py
   ├── alerting.py
   ├── daily_update.py
   ├── requirements.txt
   └── deploy_and_run.bat
   └── setup_postgresql.bat
   └── setup_postgresql.bat
   ```


### Exécution des Tests

Pour exécuter les tests, utilisez la commande suivante depuis la racine du projet :

```sh
"C:\chemin\vers\env_virtuel\Scripts\python.exe" -m unittest discover -s tests
```


# Documentation de Configuration et de Planification des Tâches

## Vue d'ensemble
Cet partie fournit des instructions pour configurer et planifier l'exécution des scripts Python `daily_update.py` et `alerting.py` à l'aide de fichiers batch sous Windows. Ces scripts doivent être exécutés dans un environnement virtuel Python.

## Prérequis

- Python installé et accessible dans le chemin système
- Un environnement virtuel Python (préalablement crée)

## Fichiers
- `run_daily_update.bat` : Configure les tâches planifiées pour exécuter `daily_update.py` toutes les 3 minutes entre 9h00 et 17h00 les jours ouvrables.
- `run_alerting.bat` : Configure une tâche planifiée pour exécuter `alerting.py` à 17h00 chaque jour ouvrable.


- Il faudra renseigner le chemin de l'environnement virtuel avant de planifier ces tâches, exemple : 

   `"C:\path\to\project\my_env"` dans la variable `PROJECT_VENV_PATH`

## Configuration et exécution des scripts

### Configuration de l'environnement virtuel
1. Créez un environnement virtuel si ce n'est pas déjà fait :
   ```bash
   python -m venv chemin\vers\votre\venv


### Fichier config.py

Ce fichier fournit des descriptions détaillées des paramètres de configuration disponibles dans le fichier `config.py`. Ce fichier contient des paramètres relatifs à la connexion à la base de données, la récupération des données des tickers boursiers, les chemins des répertoires pour sauvegarder les fichiers, ainsi que la configuration des e-mails pour les notifications.

#### Configuration de la Base de Données

Le dictionnaire `DB_CONFIG` contient les paramètres nécessaires pour se connecter à une base de données PostgreSQL. Chaque clé du dictionnaire est décrite ci-dessous :

- `dbname`: Nom de la base de données à laquelle se connecter.
- `user`: Nom d'utilisateur de l'utilisateur de la base de données.
- `password`: Mot de passe pour l'utilisateur de la base de données.
- `host`: Nom d'hôte du serveur de base de données.
- `port`: Numéro de port sur lequel le serveur de base de données fonctionne.

Exemple:
```python
DB_CONFIG = {
    "dbname": "datawarehouse",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}
```

Le dictionnaire `TICKERS` contient toutes les actions du CAC40 à récupèrer.

`SAVE_DIRECTORY` et `SAVE_EXCEL` sont les dossiers où seront stockés les données brutes des actions du CAC40 (datalake) et le dossier où l'on créera le fichier excel par la suite respectivement.

`EMAIL_CONFIG` contient les paramètres nécessaires pour l'envoi d'e-mails via un serveur SMTP. Ces paramètres sont particulièrement utiles pour l'envoi de notifications ou d'alertes automatisées. 

**IMPORTANT** : créer un compte outlook si jamais vous voulez effectuer l'alerting avec un compte personnel, et définissez  le ensuite dans `config.py`.

Lors de la reception du mail, regarder dans les spams au cas où.

Si vous rencontrez une erreur lors de l'envoi, vérifiez les paramètres de votre compte et lisez la documentation.


   - sender_email: L'adresse e-mail qui apparaîtra comme expéditeur.
   - receiver_email: L'adresse e-mail du destinataire.
   - smtp_server: Adresse du serveur SMTP.
   - smtp_port: Numéro de port utilisé par le serveur SMTP.
   - smtp_user: Nom d'utilisateur pour l'authentification au serveur SMTP.
   - smtp_password: Mot de passe pour l'authentification au serveur SMTP.

### Configuration dans le Planificateur de Tâches
1. Planifier `daily_update.py`

    - Ouvrez le Planificateur de Tâches Windows.
    - Cliquez sur "Créer une tâche" dans le volet de droite.
    - Nommez la tâche (par exemple, Daily Update).
    - Cochez "Exécuter avec les privilèges les plus élevés".
    - Sous l'onglet "Déclencheurs", ajoutez un nouveau déclencheur :
        - Commencez la tâche "Quotidiennement".
        - Réglez l'heure de début à 09:00.
        - Cochez "Répéter la tâche toutes les" et choisissez "3 minutes", pour une durée de "1 jour".
    - Sous l'onglet "Actions", ajoutez une nouvelle action :
        - Action: "Démarrer un programme".
        - Programme/script: Naviguez et sélectionnez run_daily_update.bat.
    - Configurez les options supplémentaires si nécessaire.
    -Enregistrez la tâche.

2. Planifier `alerting.py`

Répétez les étapes ci-dessus pour alerting.py, en ajustant le déclencheur pour exécuter la tâche une fois par jour à 17:00.

### Notes Additionnelles

- **Utilisez des chemins absolus** lors de la configuration des actions dans le Planificateur de tâches pour éviter tout problème lié au chemin.
- **Testez chaque script** après sa configuration pour s'assurer qu'il fonctionne comme prévu.
- **Vérifiez les logs** du Planificateur de tâches en cas d'échec des tâches planifiées pour diagnostiquer les problèmes.

### Ameliorations potentiel

- Ne pas stocker en dur les données de configurations pour des raisons de sécurité.

- Utilisation de variables d'environnements.

- Dockerisation du projet pour éviter de tout setup en local et pour la portabilité.

### Futures améliorations
- Streamlit pour l'UI

- Dockerisation du projet

- incorporation du retrieve en temps réel des données (à réfléchir comment)