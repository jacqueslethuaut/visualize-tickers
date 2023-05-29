"""
Author: Jacques Le Thuaut
Title: Implementation of pandas_datareader library
File: finance.py
"""

import pandas_datareader.data as pdr
import pandas as pd
import plotly.graph_objects as go

def get_history(ticker, period, start, end, key):
    """
     Get historical data for a ticker. This is a wrapper around pdr. DataReader. The API key is required to access the API
     
     @param ticker - ticker to get historical data for
     @param period - period of data to get in seconds ( 1 minute by default )
     @param start - start time of historical data in unix timestamp format ( YYYY - MM - DD HH : MM : SS )
     @param end - end time of historical data in unix timestamp format ( YYYY - MM - DD HH : MM : SS )
     @param key - API key to access the API ( string )
     
     @return PDR data reader ( instance of pdr. DataReader ) that can be used to read historical data
    """
    
    return pdr.DataReader(name=ticker, data_source=period, start=start, end=end, api_key=key)
    

def get_history_and_plot(ticker, period, start, end, key):
    """
     Get AAPL history and plot it. This is a wrapper for get_history that creates a plot and returns the plot
     
     @param ticker - ticker to get history for
     @param period - period of the history ( must be between start and end )
     @param start - start date of the history ( must be between start and end )
     @param end - end date of the history ( must be between start and end )
     @param key - key to use for key generation ( str )
     
     @return pandas DataFrame with open high low close as columns and candlestick as rows. Each row is a column of the
    """
    data = get_history(ticker, period, start, end, key)
    
    fig = go.Figure()

    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color= 'cyan', decreasing_line_color= 'gray'
    )])

    fig.update_layout(
        xaxis_rangeslider_visible=True,
        title='AAPL : Prix à la fermeture par jour',
        yaxis_title='AAPL Stock',
    )

    fig.show()
    
    return data

