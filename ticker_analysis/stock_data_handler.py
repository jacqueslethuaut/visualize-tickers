"""
Author: Jacques LE THUAUT
Title: Implementation of a stock data hadler based on alpha_vantage and pickle for caching
File: stock_data_handler.py
"""
import pandas as pd
import numpy as np
import pickle
import os

from alpha_vantage.timeseries import TimeSeries

class StockDataHandler:
    def __init__(self, ticker, period, start_date, end_date, api_key, data_dir='stock_data'):
        self.ticker = ticker
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.file_path = os.path.join(self.data_dir, f'{self.ticker}_{self.start_date}_{self.end_date}.pkl')

    def download_data(self):
        # Download historical market data
        ts = TimeSeries(key=self.api_key, output_format='pandas')

        data = None
        match self.period:
            case 'daily':
                data, metadata = ts.get_daily(symbol=self.ticker, outputsize='full')
            case 'daily_adjusted':
                data, metadata = ts.get_daily_adjusted(symbol=self.ticker, outputsize='full')

        if data is not None:
            data['return'] = data['4. close'].pct_change()
            data['volatility'] = data['return'].rolling(21).std() * np.sqrt(252)  # annualized volatility

        self.data = data
        return self.data

    def save_data(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                self.data = pickle.load(f)
            return self.data
        else:
            raise ValueError(f"No data for {self.ticker} from {self.start_date} to {self.end_date} found.")

    def get_data(self):
        if os.path.exists(self.file_path):
            print('Loading data from disk.')
            return self.load_data()
        else:
            print('Downloading and saving data.')
            self.download_data()
            self.save_data()
            return self.data
