from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

import datetime
from dashboard_styles import center

app = Dash(__name__)
server = app.server

start_date = '2020-01-01'
end_date = datetime.date.today()

def serve_layout():
    df = pd.read_csv('sensor_data.csv')
    print(df)
    return html.Div(children=[
        html.H1(children='Remote data logger', style=center()),

        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=datetime.date(1970, 1, 1),
                max_date_allowed=datetime.date.today(),
                start_date=start_date,
                end_date=end_date,
            ),
        ], 
        style=center()),
        html.H3(children='Select date range', style=center()),

        dcc.Graph(
            figure={
                'data': [go.Scatter(x=df['time'], y=df['uv'])],
                'layout': {'title': 'UV Index'}
        }),

        dcc.Graph(
            figure={
                'data': [go.Scatter(x=df['time'], y=df['temperature'])],
                'layout': {'title': 'Temperature [°C]'}
        }),

        dcc.Graph(
            figure={
                'data': [go.Scatter(x=df['time'], y=df['humidity'])],
                'layout': {'title': 'Humidity [g/kg]'}
        }),
])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=False)
