-- Créer la base de données
CREATE DATABASE datawarehouse_test;

-- Se connecter à la base de données
\c datawarehouse_test;

-- Création du schéma stocks
CREATE SCHEMA stocks AUTHORIZATION postgres;