from financial_package.get_historical_data import CAC40HistoricalData
from financial_package.insert_into_postgres import PostgresInserter
from config import DB_CONFIG, TICKERS, SAVE_DIRECTORY
import os

def setup_directory(path: str):
    """Crée un répertoire s'il n'existe pas déjà."""
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    # Définir les répertoires de sauvegarde
    setup_directory(SAVE_DIRECTORY)

    # Création d'une instance de CAC40HistoricalData
    cac40_data = CAC40HistoricalData(tickers_list=TICKERS, save_path=SAVE_DIRECTORY)
    cac40_data.process_and_save_all()

    # Création d'une instance de PostgresInserter
    inserter = PostgresInserter(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        save_path=SAVE_DIRECTORY
    )
    # inserter.delete_data(), pour relancer le traitement, vider les tables avant.
    inserter.process_and_insert_all()

if __name__ == "__main__":
    try : 
        main()
    except Exception as e:
        print(f"Error in main: {e}")