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


### Détails du Script Batch (`deploy_and_run.bat`)

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

Ce guide et ce script batch devraient vous aider à configurer facilement votre environnement de développement.
