"""
Author: Jacques Le Thuaut
Title: Implementation of pandas_datareader library
File: finance.py
"""

import pandas_datareader.data as pdr
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objects as go

from alpha_vantage.timeseries import TimeSeries
from plotly.subplots import make_subplots

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
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color= 'cyan', decreasing_line_color= 'gray'
    )])

    fig.update_layout(
        xaxis_rangeslider_visible=True,
        title='AAPL : Prix à la fermeture par jour',
        yaxis_title='AAPL Stock',
    )

    fig.show()
    
    return data


def get_history_plot(ticker, period, key):
    """
     Get history plot for ticker. This function is used to plot historical trading data for a given ticker
     
     @param ticker - ticker to get data for
     @param period - period to get data for e. g.
     @param key - time series key to use
     
     @return subplots of candlestick plot with data
    """
    ts = TimeSeries(key=key, output_format='pandas')

    match period:
        case 'av-daily-adjusted':
            data, metadata = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
        case 'av-daily':
            data, metadata = ts.get_daily(symbol=ticker, outputsize='full')

    data['return'] = data['4. close'].pct_change()
    data['volatility'] = data['return'].rolling(21).std()

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.02)

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['1. open'],
        high=data['2. high'],
        low=data['3. low'],
        close=data['4. close'],
        increasing_line_color= 'cyan', decreasing_line_color= 'gray',
        name='AAPL'
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['volatility'], 
        mode='lines', 
        line=dict(width=1.5),
        name='Volatility'
    ), row=2, col=1)

    fig.update_layout(
        xaxis_rangeslider_visible=True,
        title='AAPL : Daily Close Prices and Volatility',
    )

    fig.show()
    return data