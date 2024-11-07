import requests
import pandas as pd
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Fetch data from the API
url = 'https://data.winnipeg.ca/resource/vrzk-mj7v.json'
response = requests.get(url)
data = pd.DataFrame(response.json())

# Data preprocessing
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['wait_time_seconds'] = pd.to_numeric(data['wait_time_seconds'], errors='coerce')
data['talk_time_seconds'] = pd.to_numeric(data['talk_time_seconds'], errors='coerce')
data = data.dropna(subset=['wait_time_seconds', 'talk_time_seconds'])
data = data.sort_values('timestamp')

# Create Dash application
app = dash.Dash(__name__)

# Initial DataTable
data_table = dash_table.DataTable(
    id='data-table',
    columns=[{"name": i, "id": i} for i in data.columns],
    data=data.to_dict('records'),
    page_size=10,
    style_table={'overflowX': 'auto'},
    style_cell={
        'textAlign': 'center',
        'padding': '5px',
        'whiteSpace': 'normal',
        'height': 'auto',
    },
)

# Application layout
app.layout = html.Div(children=[
    html.H1(children='Winnipeg 311 Call Wait Times Dashboard'),

    html.Div([
        html.H2('Select Date Range'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=data['timestamp'].min().date(),
            end_date=data['timestamp'].max().date()
        )
    ]),

    html.H2(children='Data Table'),
    data_table,

    html.H2(children='Wait Time and Talk Time Over Time'),
    dcc.Graph(
        id='wait-talk-time-graph'
    )
])


# Callback to update data and graph
@app.callback(
    [Output('data-table', 'data'),
     Output('wait-talk-time-graph', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_data(start_date, end_date):
    # Filter data based on selected date range
    filtered_data = data[(data['timestamp'] >= start_date) & (data['timestamp'] <= end_date)]

    # Update DataTable data
    table_data = filtered_data.to_dict('records')

    # Update figure
    fig = px.line(
        filtered_data,
        x='timestamp',
        y=['wait_time_seconds', 'talk_time_seconds'],
        labels={
            'timestamp': 'Timestamp',
            'value': 'Seconds',
            'variable': 'Metric'
        },
        title='Wait Time and Talk Time Over Time'
    )
    fig.update_layout(
        xaxis_title='Timestamp',
        yaxis_title='Time (Seconds)',
        legend_title='Metric',
        hovermode='x unified'
    )

    return table_data, fig


if __name__ == '__main__':
    app.run_server(debug=True)
