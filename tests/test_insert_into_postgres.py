import unittest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from financial_package.insert_into_postgres import PostgresInserter

class TestPostgresInserter(unittest.TestCase):
    """
    Test case for the PostgresInserter class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup test environment for PostgresInserter tests.
        """
        cls.db_config = {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "host": "localhost",
            "port": "5432"
        }
        cls.save_path = "./test_data"
        if not os.path.exists(cls.save_path):
            os.makedirs(cls.save_path)
        cls.inserter = PostgresInserter(
            dbname=cls.db_config['dbname'],
            user=cls.db_config['user'],
            password=cls.db_config['password'],
            host=cls.db_config['host'],
            port=cls.db_config['port'],
            save_path=cls.save_path
        )

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test environment after tests are done.
        """
        for filename in os.listdir(cls.save_path):
            file_path = os.path.join(cls.save_path, filename)
            os.remove(file_path)
        os.rmdir(cls.save_path)

    @patch('psycopg2.connect')
    def test_connect(self, mock_connect):
        """
        Test that the connect method establishes a database connection.
        """
        mock_connect.return_value.cursor.return_value = MagicMock()
        self.inserter.connect()
        self.assertIsNotNone(self.inserter.conn)
        self.assertIsNotNone(self.inserter.cursor)

    @patch('psycopg2.connect')
    def test_create_table(self, mock_connect):
        """
        Test that create_table creates a table in the database.
        """
        mock_connect.return_value.cursor.return_value = MagicMock()
        df = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2020', periods=5),
            'Open': [1, 2, 3, 4, 5],
            'High': [2, 3, 4, 5, 6],
            'Low': [0.5, 1.5, 2.5, 3.5, 4.5],
            'Close': [1.5, 2.5, 3.5, 4.5, 5.5],
            'Volume': [100, 200, 300, 400, 500],
            'Dividends': [0, 0, 0, 0, 0],
            'Stock_Splits': [0, 0, 0, 0, 0]
        })
        self.inserter.connect()
        self.inserter.create_table('AAPL', df)
        self.inserter.close()
        self.assertTrue(mock_connect.called)

    @patch('psycopg2.connect')
    def test_insert_data(self, mock_connect):
        """
        Test that insert_data inserts data into the database table.
        """
        mock_connect.return_value.cursor.return_value = MagicMock()
        df = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2020', periods=5),
            'Open': [1, 2, 3, 4, 5],
            'High': [2, 3, 4, 5, 6],
            'Low': [0.5, 1.5, 2.5, 3.5, 4.5],
            'Close': [1.5, 2.5, 3.5, 4.5, 5.5],
            'Volume': [100, 200, 300, 400, 500],
            'Dividends': [0, 0, 0, 0, 0],
            'Stock_Splits': [0, 0, 0, 0, 0]
        })
        self.inserter.connect()
        self.inserter.create_table('AAPL', df)
        self.inserter.insert_data('AAPL', df)
        self.inserter.close()
        self.assertTrue(mock_connect.called)

    @patch('psycopg2.connect')
    def test_delete_data(self, mock_connect):
        """
        Test that delete_data deletes data from the database tables.
        """
        mock_connect.return_value.cursor.return_value = MagicMock()
        self.inserter.connect()
        self.inserter.delete_data()
        self.inserter.close()
        self.assertTrue(mock_connect.called)

if __name__ == "__main__":
    unittest.main()
