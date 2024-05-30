Instructions pour configurer PostgreSQL et exécuter le script SQL :

1. Téléchargez et installez PostgreSQL depuis https://www.postgresql.org/download/.

2. Pendant l'installation, notez le mot de passe que vous définissez pour l'utilisateur `postgres`, mettez `root` pour faciliter la suite.

3. Modifiez le script batch `setup_postgresql.bat` :
   - Remplacez `C:\Program Files\PostgreSQL\13\bin` par le chemin où PostgreSQL est installé, si différent.
   - Remplacez `C:\path\to\your\script\setup_database.sql` par le chemin réel où se trouve votre script SQL.

4. Exécutez le script batch `setup_postgresql.bat` en tant qu'administrateur :
   - Ouvrez l'invite de commande (cmd) ou le terminal (PowerShell) sur votre ordinateur.
   - Accédez au répertoire où se trouve le script batch.
   - Exécutez le script en tapant `setup_postgresql.bat`.

5. Le script batch ajoutera PostgreSQL au PATH, se connectera à PostgreSQL, et exécutera le script SQL pour créer la base de données `datawarehouse`.

6. Executez le script et rentrez le mot de passe `root`.

7. Une fois le script exécuté, vous pouvez vérifier que la base de données et le schéma `stocks` ont été crées en utilisant les commandes PostgreSQL appropriées :

      ```
      Tapez psql dans l'invite de commandes

      \l -- Pour lister les bases de données

      \c mydatabase -- Pour se connecter à la base de données

      \dt -- Pour lister les tables

      SELECT * FROM mytable; -- Pour voir les données dans la table
      ```

8. **RECOMMANDATIONS** 

      Installez DBeaver pour se connecter à la base de données et avoir une interface pour mieux visualiser les données.