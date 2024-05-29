-- Créer la base de données
CREATE DATABASE datawarehouse;

-- Se connecter à la base de données
\c datawarehouse;

-- Création du schéma stocks
CREATE SCHEMA stocks AUTHORIZATION postgres;