from datetime import datetime
import pandas as pd
import numpy as np
import sys
import logging

class StockDataETL:
    def __init__(self, df):
        self.df = df.astype(str).tail(1)
        self.type_error = []
        self.df_invalid = pd.DataFrame()

    def check_legal_characters(self):
        logging.info("Starting check_legal_characters method.")
        try:
            pd.to_datetime(self.df['Date'])
            print("'Date': OK")
        except ValueError:
            print("'Date': PAS OK")
            self.type_error.append("'Date' format")
        except KeyError:
            logging.error("Column 'Date' not found in the DataFrame.")
            self.type_error.append("'Date' column missing")

        for column in self.df.columns:
            if column not in ('Date', 'date_modification'):
                if self.df[column].str.match(r'^-?\d*\.?\d*$').all():
                    print(f"'{column}': OK")
                else:
                    print(f"'{column}': PAS OK")
                    self.type_error.append(f"'{column}' format")
        logging.info("Finished check_legal_characters method.")

    def recast_columns(self):
        logging.info("Starting recast_columns method.")
        self.df['Date'] = pd.to_datetime(self.df['Date'])

        for column in self.df.columns:
            if column != 'Date':
                if column in ['Open', 'High', 'Low', 'Close']:
                    self.df[column] = pd.to_numeric(self.df[column])
                elif column == 'Volume':
                    self.df[column] = self.df[column].astype(int)
                elif column in ['Dividends', 'Stock_Splits']:
                    self.df[column] = self.df[column].astype(float)
                elif column == 'date_modification':
                    self.df[column] = pd.to_datetime(self.df[column])

        logging.info("Finished recast_columns method.")

    def filter_aberrant_values(self):
        logging.info("Starting filter_aberrant_values method.")
        
        price_columns = ['Open', 'High', 'Low', 'Close']
        invalid_price_rows = self.df[(self.df[price_columns] < 0).any(axis=1)]
        self.df_invalid = pd.concat([self.df_invalid, invalid_price_rows])
        self.df = self.df[~self.df.index.isin(invalid_price_rows.index)]

        invalid_date_rows = self.df[self.df['Date'] < '1987-12-31']
        self.df_invalid = pd.concat([self.df_invalid, invalid_date_rows])
        self.df = self.df[~self.df.index.isin(invalid_date_rows.index)]

        current_date = np.datetime64(datetime.now().date())
        invalid_future_date_rows = self.df[self.df['Date'] > current_date]
        self.df_invalid = pd.concat([self.df_invalid, invalid_future_date_rows])
        self.df = self.df[~self.df.index.isin(invalid_future_date_rows.index)]

        if invalid_date_rows.shape[0] > 0 or invalid_future_date_rows.shape[0] > 0:
            self.type_error.append('Date val')

        if invalid_price_rows.shape[0] > 0:
            self.type_error.append('Num val')

        logging.info("Finished filter_aberrant_values method.")

    def save_invalid_data(self):
        logging.info("Starting save_invalid_data method.")
        if not self.df_invalid.empty:
            self.df_invalid['type_error'] = ', '.join(self.type_error)
            self.df_invalid.to_excel('unvalid_data.xlsx', index=False)
        logging.info("Finished save_invalid_data method.")

    def process(self):
        logging.info("Starting process method.")
        self.check_legal_characters()
        if self.type_error:
            self.df['type_error'] = ', '.join(self.type_error)
            logging.error("Type errors found, exiting process.")
            return None

        self.recast_columns()
        self.filter_aberrant_values()
        if not self.df_invalid.empty:
            logging.error("Invalid data found, exiting process.")
            self.save_invalid_data()
            return None
        
        logging.info("Finished process method.")
        return self.df
