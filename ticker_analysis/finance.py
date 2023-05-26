# tickerazor.py

import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd

def get_history(ticker, period, start, end, key):
    return web.DataReader(name=ticker, data_source=period, start=start, end=end, api_key=key)
    

def get_history_and_plot(ticker, period, start, end, key):
    df = get_history(ticker, period, start, end, key)
    
    plt.figure(figsize=(16, 9))
    plt.plot(df['close'])
    plt.xlabel("Date")
    plt.ylabel("Adjusted Close Price")
    plt.title(f"{ticker} Price Data")
    plt.grid(True)
    plt.show()
    
    return df

