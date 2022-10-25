import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pandas_datareader import data as wb
from datetime import datetime as dt
from flask_app import appp

appp.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'KO'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Amazón', 'value': 'AMZN'}
        ],
        value='KO'
    ),
    dcc.Graph(id='my-graph')
    
], style={'width': '500'})

@appp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    stock = wb.DataReader(selected_dropdown_value,data_source='bloomberg', start='2022-01-05') #año-mes-dia
    return {
        'data': [{
            'x': stock.index,
            'y': stock.Close
        }],
        'layout': {'margin': {'l': 40, 'r': 10, 't': 20, 'b': 30}}
    }