"""
Author: Jacques LE THUAUT
Title: Implementation of a dash wrapper
File: finance.py
"""

import numpy as np
import plotly.graph_objects as go
import dash

from dash.dependencies import Input, Output

from jupyter_dash import JupyterDash
from dash import html
from dash import dcc
from dash import callback_context


class FinanceApp:
    def __init__(self):
        self.app = JupyterDash('Finance App')
        self.data = None
        self.zoom_factor = 0.2  # Adjust this to change the amount of zoom per click

        # Define the layout
        self.app.layout = html.Div([
            dcc.Graph(
                id='graph',
                config={'displayModeBar': False}
            ),
            html.Div([
                dcc.RangeSlider(
                    id='slider',
                    min=0,
                    max=100,
                    value=[0, 100]
                )
            ]),
            html.Button('Zoom In', id='zoom-in-button'),
            html.Button('Zoom Out', id='zoom-out-button')
        ])

        @self.app.callback(
            Output('graph', 'figure'),
            Output('slider', 'max'),
            Output('slider', 'value'),
            Input('slider', 'value'),
            Input('zoom-in-button', 'n_clicks'),
            Input('zoom-out-button', 'n_clicks')
        )
        def update_figure(selected_range, zoom_in_n_clicks, zoom_out_n_clicks):
            ctx = dash.callback_context
            zoom_in_clicked = ctx.triggered[0]['prop_id'] == 'zoom-in-button.n_clicks'
            zoom_out_clicked = ctx.triggered[0]['prop_id'] == 'zoom-out-button.n_clicks'

            if self.data is not None:
                filtered_data = self.data.iloc[selected_range[0]:selected_range[1]]

                # Create a candlestick chart
                fig = go.Figure(data=[go.Candlestick(
                    x=filtered_data.index,
                    open=filtered_data['1. open'],
                    high=filtered_data['2. high'],
                    low=filtered_data['3. low'],
                    close=filtered_data['4. close'],
                    increasing_line_color= 'cyan', decreasing_line_color= 'gray'
                )])

                # Add a line chart for volatility
                fig.add_trace(go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['volatility'],
                    mode='lines',
                    line=dict(width=1.5),
                    name='Volatility'
                ))

                fig.update_layout(
                    title='Daily Close Prices and Volatility',
                    yaxis_title='Volatility',
                    yaxis2=dict(title='Price', overlaying='y', side='left'),
                    xaxis=dict(rangeslider=dict(visible=False)),
                    yaxis2_range = [min(filtered_data['4. close']), max(filtered_data['4. close'])],
                    yaxis_range = [min(filtered_data['volatility']), max(filtered_data['volatility'])],
                )

                # Handle zoom
                if zoom_in_clicked or zoom_out_clicked:
                    range_len = selected_range[1] - selected_range[0]
                    range_mid = selected_range[0] + range_len / 2
                    if zoom_in_clicked:
                        new_range = [int(range_mid - self.zoom_factor * range_len / 2),
                                     int(range_mid + self.zoom_factor * range_len / 2)]
                    else:  # zoom_out_clicked
                        new_range = [max(0, int(range_mid - (1 + self.zoom_factor) * range_len / 2)),
                                     min(len(self.data), int(range_mid + (1 + self.zoom_factor) * range_len / 2))]
                    return fig, len(self.data.index), new_range

                return fig, len(self.data.index), [0, len(self.data.index)]
            
            return go.Figure(), 100, [0, 100]
        

    def show(self):
        self.app.run_server(mode='inline')
        
    
    def load_stock_data(self, data):
        self.data = data
        self.app.layout.children[1].children[0].max = len(data.index)
        self.app.layout.children[1].children[0].value = [0, len(data.index)]
    
