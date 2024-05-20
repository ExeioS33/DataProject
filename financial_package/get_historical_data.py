import os
import yfinance as yf
from datetime import datetime
import pandas as pd
import random
from typing import List
from typing import Tuple

import os
import yfinance as yf
from datetime import datetime
import pandas as pd
from typing import List
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CAC40HistoricalData:
    """
    Retrieves and saves historical data for a list of CAC 40 stock symbols.

    Attributes:
        tickers_list (List[str]): List of stock symbols to retrieve.
        save_path (str): Path to the directory where CSV files will be saved.
    """

    def __init__(self, tickers_list: List[str], save_path: str = "."):
        """
        Initializes the class with a list of stock symbols and a save path.

        Args:
            tickers_list (List[str]): List of stock symbols to retrieve.
            save_path (str): Path to the directory where CSV files will be saved.
        """
        self.tickers_list = tickers_list
        self.save_path = save_path

        # Create the save directory if it doesn't exist
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            logging.info(f"Created directory {self.save_path} for saving CSV files.")

    def fetch_data(self, ticker_symbol: str) -> pd.DataFrame:
        """
        Retrieves historical data for a given stock symbol.

        Args:
            ticker_symbol (str): The stock symbol to process.
        
        Returns:
            pd.DataFrame: A DataFrame containing the historical data, sorted by descending date.

        Raises:
            Exception: If there is an error fetching data from yfinance.
        """
        try:
            ticker = yf.Ticker(ticker_symbol)
            data = ticker.history(period="max")
            data.index = data.index.tz_localize(None)
            logging.info(f"Successfully fetched data for {ticker_symbol}.")
            return data
        except Exception as e:
            logging.error(f"Error fetching data for {ticker_symbol}: {e}")
            raise

    def save_to_csv(self, data: pd.DataFrame, ticker_symbol: str) -> None:
        """
        Saves the data to a CSV file, named after the stock symbol.

        Args:
            data (pd.DataFrame): The data to save.
            ticker_symbol (str): The stock symbol used to name the file.

        Raises:
            Exception: If there is an error saving the data to CSV.
        """
        try:
            # Rename the column "Stock Splits" to "Stock_Splits"
            data = data.rename(columns={"Stock Splits": "Stock_Splits"})
            
            filename = f"{ticker_symbol}_Historical_Data.csv"
            filepath = os.path.join(self.save_path, filename)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data['date_modification'] = current_date
            data['date_modification'] = pd.to_datetime(data['date_modification'])
            data.to_csv(filepath)
            logging.info(f"Saved historical data for {ticker_symbol} in {filepath}")
        except Exception as e:
            logging.error(f"Error saving data for {ticker_symbol} to CSV: {e}")
            raise

    def process_and_save_all(self) -> None:
        """
        Processes and saves historical data for all stock symbols in the list.
        """
        for ticker_symbol in self.tickers_list:
            try:
                data = self.fetch_data(ticker_symbol)
                self.save_to_csv(data, ticker_symbol)
            except Exception as e:
                logging.error(f"Failed to process and save data for {ticker_symbol}: {e}")


class StockHistoricalData(CAC40HistoricalData):
    """
    Derived class from CAC40HistoricalData to retrieve and save historical data 
    for a specific stock into an Excel file. (Not actually used)
    """
    def __init__(self, tickers_list: List[str], save_path: str = ".") -> None:
        super().__init__(tickers_list, save_path)  # Initializes with the list of tickers

    def fetch_random_data(self) -> Tuple[pd.DataFrame, str]:
        """
        Selects a random ticker from the list and retrieves its historical data.
        
        Returns:
            Tuple[pd.DataFrame, str]: A tuple containing the historical data and the selected ticker symbol.
        """
        random_ticker = random.choice(self.tickers_list)  # Selects a random ticker
        return self.fetch_data(random_ticker), random_ticker

    def save_to_excel(self, filename: str = None) -> None:
        """
        Saves the historical data for a randomly selected ticker to an Excel file.
        
        Args:
            filename (str, optional): The filename for the Excel file. If not provided, a name is generated.
        """
        data, ticker = self.fetch_random_data()
        if filename is None:
            filename = f"{ticker}_Historical_Data.xlsx"
        data.index = data.index.strftime("%Y-%m-%d")
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['date_modification'] = current_date
        full_path = os.path.join(self.save_path, filename)
        data.to_excel(full_path)
        print(f"Saved historical data for {ticker} at {full_path}.")
