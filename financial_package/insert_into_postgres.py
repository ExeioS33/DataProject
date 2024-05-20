import os
import psycopg2
import pandas as pd
from typing import List
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PostgresInserter:
    """
    Inserts data from CSV files into PostgreSQL tables.

    Attributes:
        dbname (str): Name of the PostgreSQL database.
        user (str): Database user.
        password (str): Password for the database user.
        host (str): Host address of the PostgreSQL server.
        port (str): Port number for the PostgreSQL server.
        save_path (str): Path to the directory containing CSV files.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str, save_path: str = "."):
        """
        Initializes the class with database connection details and save path.

        Args:
            dbname (str): Name of the PostgreSQL database.
            user (str): Database user.
            password (str): Password for the database user.
            host (str): Host address of the PostgreSQL server.
            port (str): Port number for the PostgreSQL server.
            save_path (str): Path to the directory containing CSV files.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.save_path = save_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connects to the PostgreSQL database and sets the connection and cursor."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            logging.info("Successfully connected to the database.")
        except psycopg2.DatabaseError as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def close(self):
        """Closes the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logging.info("Database connection closed.")

    def create_table(self, table_name: str, df: pd.DataFrame):
        """
        Creates a PostgreSQL table with the same structure as the DataFrame.

        Args:
            table_name (str): Name of the table to create.
            df (pd.DataFrame): DataFrame with the data structure.

        Raises:
            Exception: If there is an error creating the table.
        """
        try:
            dtype_mapping = {
                'int64': 'INTEGER',
                'float64': 'FLOAT',
                'datetime64[ns]': 'TIMESTAMP',
                'object': 'TEXT'
            }
            columns = []
            for col in df.columns:
                col_type = dtype_mapping.get(str(df[col].dtype), 'TEXT')
                columns.append(f'"{col}" {col_type}')
            columns_str = ", ".join(columns)
            create_table_query = f'CREATE TABLE IF NOT EXISTS stocks."{table_name}" ({columns_str});'
            self.cursor.execute(create_table_query)
            self.conn.commit()
            logging.info(f"Table {table_name} created successfully.")
        except psycopg2.Error as e:
            logging.error(f"Error creating table {table_name}: {e}")
            self.conn.rollback()

    def insert_data(self, table_name: str, df: pd.DataFrame):
        """
        Inserts data from the DataFrame into the PostgreSQL table.

        Args:
            table_name (str): Name of the table to insert data into.
            df (pd.DataFrame): DataFrame with the data to insert.

        Raises:
            Exception: If there is an error inserting the data.
        """
        try:
            columns = ", ".join(f'"{col}"' for col in df.columns)
            values = ", ".join(["%s"] * len(df.columns))
            insert_query = f'INSERT INTO stocks."{table_name}" ({columns}) VALUES ({values})'
            self.cursor.executemany(insert_query, df.values.tolist())
            self.conn.commit()
            logging.info(f"Data inserted into table {table_name} successfully.")
        except psycopg2.Error as e:
            logging.error(f"Error inserting data into table {table_name}: {e}")
            self.conn.rollback()

    def process_and_create_tables(self):
        """
        Processes all CSV files in the save path and creates the tables in PostgreSQL.

        Raises:
            Exception: If there is an error processing the CSV files.
        """
        try:
            for filename in os.listdir(self.save_path):
                if filename.endswith(".csv"):
                    file_path = os.path.join(self.save_path, filename)
                    table_name = self.extract_ticker(filename)
                    df = pd.read_csv(file_path)
                    self.create_table(table_name, df)
                    logging.info(f"Table created for {filename} as {table_name}.")
        except Exception as e:
            logging.error(f"Error processing and creating tables: {e}")

    def process_and_insert_data(self):
        """
        Processes all CSV files in the save path and inserts the data into PostgreSQL.

        Raises:
            Exception: If there is an error processing the CSV files.
        """
        try:
            for filename in os.listdir(self.save_path):
                if filename.endswith(".csv"):
                    file_path = os.path.join(self.save_path, filename)
                    table_name = self.extract_ticker(filename)
                    df = pd.read_csv(file_path)
                    self.insert_data(table_name, df)
                    logging.info(f"Data from {filename} inserted into table {table_name}.")
        except Exception as e:
            logging.error(f"Error processing and inserting data: {e}")

    def process_and_insert_all(self):
        """
        Processes and inserts data from all CSV files in the save path into PostgreSQL.
        """
        try:
            self.connect()
            self.process_and_create_tables()
            self.process_and_insert_data()
        except Exception as e:
            logging.error(f"Error in process_and_insert_all: {e}")
        finally:
            self.close()

    def extract_ticker(self, filename: str) -> str:
        """
        Extracts the ticker symbol from the filename.

        Args:
            filename (str): The name of the file to process.

        Returns:
            str: The extracted ticker symbol.
        """
        ticker = filename.split('_')[0]
        return ticker

    def delete_data(self):
        """
        Deletes data from all tables corresponding to the CSV files in the save path.

        Raises:
            Exception: If there is an error deleting the data.
        """
        try:
            self.connect()
            for filename in os.listdir(self.save_path):
                if filename.endswith(".csv"):
                    table_name = self.extract_ticker(filename)
                    delete_query = f'DELETE FROM stocks."{table_name}";'
                    self.cursor.execute(delete_query)
                    self.conn.commit()
                    logging.info(f"Data deleted from table {table_name}.")
        except psycopg2.Error as e:
            logging.error(f"Error deleting data from table {table_name}: {e}")
            self.conn.rollback()
        finally:
            self.close()
