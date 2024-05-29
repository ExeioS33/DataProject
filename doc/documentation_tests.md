# Documentation des test

1. Tests pour CAC40HistoricalData

    - Test d'initialisation :
        Vérifie que l'instance est correctement initialisée avec les attributs tickers_list et save_path.
        Assurez-vous que le répertoire de sauvegarde est créé s'il n'existe pas déjà.

    - Test de récupération des données :
        Vérifie que la méthode fetch_data récupère les données historiques pour un symbole boursier donné.
        Assurez-vous que les données sont sous forme de DataFrame et contiennent les colonnes attendues.

    - Test de sauvegarde des données :
        Vérifie que la méthode save_to_csv enregistre correctement les données dans un fichier CSV.
        Assurez-vous que les fichiers sont nommés correctement et enregistrés dans le répertoire spécifié.
        Vérifie que la colonne "Stock Splits" est renommée en "Stock_Splits".

    - Test de traitement et de sauvegarde de tous les tickers :
        Vérifie que la méthode process_and_save_all traite et enregistre les données pour tous les tickers dans tickers_list.

2. Tests pour PostgresInserter

    - Test de connexion à la base de données :
        Vérifie que la méthode connect établit correctement une connexion à la base de données.
        Assurez-vous que la connexion et le curseur sont créés.

    - Test de création de table :
        Vérifie que la méthode create_table crée correctement une table dans la base de données avec la structure du DataFrame fourni.
        Assurez-vous que la table est créée avec les types de données corrects.

    - Test d'insertion des données :
        Vérifie que la méthode insert_data insère correctement les données du DataFrame dans la table spécifiée.
        Assurez-vous que les données sont insérées correctement et que les types de données sont respectés.

    - Test de traitement et de création des tables :
        Vérifie que la méthode process_and_create_tables crée des tables pour tous les fichiers CSV dans le répertoire spécifié.

    - Test de traitement et d'insertion des données :
        Vérifie que la méthode process_and_insert_data insère les données de tous les fichiers CSV dans les tables correspondantes.

    - Test de suppression des données :
        Vérifie que la méthode delete_data supprime correctement les données des tables correspondant aux fichiers CSV dans le répertoire spécifié.