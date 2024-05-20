import unittest
import os
import pandas as pd
from unittest.mock import patch
from financial_package.get_historical_data import CAC40HistoricalData

class TestCAC40HistoricalData(unittest.TestCase):
    """
    Test case for the CAC40HistoricalData class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup test environment for CAC40HistoricalData tests.
        """
        cls.tickers = ['AAPL', 'MSFT']
        cls.save_path = "./test_data"
        if not os.path.exists(cls.save_path):
            os.makedirs(cls.save_path)
        cls.cac40_data = CAC40HistoricalData(cls.tickers, cls.save_path)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test environment after tests are done.
        """
        for filename in os.listdir(cls.save_path):
            file_path = os.path.join(cls.save_path, filename)
            os.remove(file_path)
        os.rmdir(cls.save_path)

    def test_initialization(self):
        """
        Test that the CAC40HistoricalData class is initialized correctly.
        """
        self.assertEqual(self.cac40_data.tickers_list, self.tickers)
        self.assertEqual(self.cac40_data.save_path, self.save_path)

    @patch('yfinance.Ticker')
    def test_fetch_data(self, mock_ticker):
        """
        Test that fetch_data retrieves data and returns a DataFrame.
        """
        mock_ticker().history.return_value = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2020', periods=5),
            'Open': [1, 2, 3, 4, 5],
            'High': [2, 3, 4, 5, 6],
            'Low': [0.5, 1.5, 2.5, 3.5, 4.5],
            'Close': [1.5, 2.5, 3.5, 4.5, 5.5],
            'Volume': [100, 200, 300, 400, 500],
            'Dividends': [0, 0, 0, 0, 0],
            'Stock Splits': [0, 0, 0, 0, 0]
        }).set_index('Date')
        data = self.cac40_data.fetch_data('AAPL')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue('Open' in data.columns)

    @patch('yfinance.Ticker')
    def test_save_to_csv(self, mock_ticker):
        """
        Test that save_to_csv saves the data correctly to a CSV file.
        """
        mock_ticker().history.return_value = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2020', periods=5),
            'Open': [1, 2, 3, 4, 5],
            'High': [2, 3, 4, 5, 6],
            'Low': [0.5, 1.5, 2.5, 3.5, 4.5],
            'Close': [1.5, 2.5, 3.5, 4.5, 5.5],
            'Volume': [100, 200, 300, 400, 500],
            'Dividends': [0, 0, 0, 0, 0],
            'Stock Splits': [0, 0, 0, 0, 0]
        }).set_index('Date')
        data = self.cac40_data.fetch_data('AAPL')
        self.cac40_data.save_to_csv(data, 'AAPL')
        self.assertTrue(os.path.exists(os.path.join(self.save_path, 'AAPL_Historical_Data.csv')))

if __name__ == "__main__":
    unittest.main()
