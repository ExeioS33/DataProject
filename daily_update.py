import logging
import os
import pandas as pd
from financial_package.get_historical_data import CAC40HistoricalData
from financial_package.postgres_utils import PostgresInserter, DataExporter
from financial_package.etl import StockDataETL
from config import DB_CONFIG, TICKERS, SAVE_DIRECTORY, SAVE_EXCEL

# Setup logging
log_directory = os.path.abspath("logs")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, "daily_update.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path,
    filemode='w'  # Overwrite the log file every time the script runs
)

def main():
    logging.info("Starting the daily data update process.")

    # Création d'une instance de CAC40HistoricalData
    cac40_data = CAC40HistoricalData(tickers_list=TICKERS, save_path=SAVE_DIRECTORY)
    logging.info("CAC40HistoricalData instance created.")

    # Création d'une instance de PostgresInserter
    inserter = PostgresInserter(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        save_path=SAVE_DIRECTORY
    )
    logging.info("PostgresInserter instance created.")

    inserter.connect()

    # Process and insert the latest data for each ticker
    for ticker in TICKERS:
        data = cac40_data.fetch_data(ticker)

        if 'Date' not in data.columns:
            logging.error(f"Column 'Date' not found in the data for ticker: {ticker}")
            continue

        etl_processor = StockDataETL(data)
        latest_data = etl_processor.process()

        if isinstance(latest_data, pd.DataFrame):
            inserter.insert_data(ticker, latest_data)
        else:
            logging.error(f"Failed to process data for ticker: {ticker}")

    inserter.close()

    logging.info("Daily data update process completed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Error in daily update: {e}", exc_info=True)
