from datetime import datetime
import traceback
import pandas as pd
import numpy as np
import sys

class StockDataETL:
    def __init__(self, df):
        self.df = df.astype(str).tail(1)
        self.type_error = []
        self.df_invalid = pd.DataFrame()

    def check_legal_characters(self):
        try:
            pd.to_datetime(self.df['Date'])
            print("'Date': OK")
        except ValueError:
            print("'Date': PAS OK")
            self.type_error.append("'Date' format")

        for column in self.df.columns:
            if column not in ('Date', 'date_modification'):
                if self.df[column].str.match(r'^-?\d*\.?\d*$').all():
                    print(f"'{column}': OK")
                else:
                    print(f"'{column}': PAS OK")
                    self.type_error.append(f"'{column}' format")

    def recast_columns(self):
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

    def filter_aberrant_values(self):
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

    def save_invalid_data(self):
        print(self.df_invalid)
        if not self.df_invalid.empty:
            self.df_invalid['type_error'] = ', '.join(self.type_error)
            self.df_invalid.to_excel('unvalid_data.xlsx', index=False)

    def process(self):
        self.check_legal_characters()
        
        if self.type_error:
            self.df['type_error'] = ', '.join(self.type_error)
            self.df.to_excel('unvalid_data.xlsx', index=False)
            sys.exit()

        self.recast_columns()
        self.filter_aberrant_values()
        self.save_invalid_data()
        
        if not self.df_invalid.empty:
            return self.df
        else: 
            print('error aberrant_values')

if __name__ == "__main__":
    # Extraction du CSV et création du DataFrame
    df = pd.read_csv('ACA.PA_Historical_Data.csv')

    # Création de l'instance de la classe et traitement des données
    etl = StockDataETL(df)
    processed_df = etl.process()
    print(processed_df)  # Utilisez le DataFrame traité comme nécessaire
