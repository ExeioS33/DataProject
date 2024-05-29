import os
import psycopg2
import pandas as pd
from typing import List
from datetime import datetime
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
        if self.cursor is None or self.conn is None:
            self.connect()
        
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


class DataExporter(PostgresInserter):
    """
    Exports intraday data from PostgreSQL tables to a single Excel file with multiple sheets.

    Attributes:
        dbname (str): Name of the PostgreSQL database.
        user (str): Database user.
        password (str): Password for the database user.
        host (str): Host address of the PostgreSQL server.
        port (str): Port number for the PostgreSQL server.
        save_path (str): Path to the directory to save the Excel files.
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
            save_path (str): Path to the directory to save the Excel files.
        """
        super().__init__(dbname, user, password, host, port, save_path)

        # Create the save directory if it doesn't exist
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            logging.info(f"Created directory {self.save_path} for saving Excel file.")

    def retrieve_data(self, table_name: str) -> pd.DataFrame:
        """
        Fetches data from a PostgreSQL table where the Date column is equal to today's date.

        Args:
            table_name (str): The name of the table to fetch data from.

        Returns:
            pd.DataFrame: A DataFrame containing the fetched data.
        """
        if self.conn is None or self.cursor is None:
            return None
        
        try:
            current_date_str = datetime.now().strftime('%Y-%m-%d 00:00:00')
            
            query = f'SELECT * FROM stocks.\"{table_name}\" WHERE "Date" = %s ORDER BY date_modification DESC;'
            self.cursor.execute(query, (current_date_str,))
            rows = self.cursor.fetchall()
            colnames = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(rows, columns=colnames)
            return df
        except psycopg2.Error as e:
            print(f"Error fetching data from table {table_name}: {e}")
            return None

    def export_to_excel(self, table_data: dict, excel_filename: str):
        """
        Exports data from PostgreSQL tables to an Excel file with each table's data in a separate sheet.
        """
        filepath = os.path.join(self.save_path, excel_filename)
        try:
            with pd.ExcelWriter(filepath) as writer:
                has_data = False
                for table_name, df in table_data.items():
                    if df is not None and not df.empty:
                        df.to_excel(writer, sheet_name=table_name, index=False)
                        logging.info(f"Exported data for table {table_name} to {excel_filename}")
                        has_data = True
                    else:
                        logging.info(f"No data to export for table {table_name}")
                if not has_data:
                    pd.DataFrame({"Info": ["No data available for any table"]}).to_excel(writer, sheet_name="Info", index=False)
                    logging.info("No data available for any table, created Info sheet.")
        except Exception as e:
            logging.error(f"Error exporting to Excel: {e}")
            raise

    def export_all_tables(self, table_names: List[str]):
        """
        Fetches and exports data for all specified tables.

        Args:
            table_names (List[str]): A list of table names to fetch and export data.
        """
        table_data = {}
        for table_name in table_names:
            df = self.retrieve_data(table_name)
            table_data[table_name] = df
        self.export_to_excel(table_data, "Today_Data.xlsx")
