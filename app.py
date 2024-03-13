import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State
from dash.dependencies import Input, Output, State, ALL
from datetime import datetime, timedelta

from test import get_booking_table

booking_table = get_booking_table()

app = Dash(__name__)

app.layout = html.Div([
    html.Label('Start Date'),
    dcc.Input(id='start_date_input', type='text', placeholder='mm.dd.yyyy'),
    html.Label('End Date'),
    dcc.Input(id='end_date_input', type='text', placeholder='mm.dd.yyyy'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date_placeholder_text='Start Period',
        end_date_placeholder_text='End Period',
        calendar_orientation='vertical',
    ),
    html.Div(id='output-container-date-picker-range'),
    html.Div(id='table-output'),  # Output container for clicked value
    booking_table,
    html.Div(id='input-container', style={'display': 'none'}, children=[
        dcc.Input(id='input1', type='text', placeholder='Input 1'),
        dcc.Input(id='input2', type='text', placeholder='Input 2'),
        html.Button('Submit', id='submit-button')
    ]),
    html.Div(id='submit-output')
])

@app.callback(
    Output('date-picker-range', 'start_date'),
    Output('date-picker-range', 'end_date'),
    Input('start_date_input', 'value'),
    Input('end_date_input', 'value')
)
def update_date_picker(start_date, end_date):
    if start_date is not None:
        start_date = datetime.strptime(start_date, '%m.%d.%Y')
    if end_date is not None:
        end_date = datetime.strptime(end_date, '%m.%d.%Y')
    return start_date, end_date

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None and end_date is not None:
        start_date_str = start_date.strftime('%m.%d.%Y') if isinstance(start_date, datetime) else start_date
        end_date_str = end_date.strftime('%m.%d.%Y') if isinstance(end_date, datetime) else end_date
        return string_prefix + 'Start Date: ' + start_date_str + ' | End Date: ' + end_date_str

@app.callback(
    Output('table-output', 'children'),
    [Input('booking-table', 'active_cell')]
)
def display_click_data(active_cell):
    if active_cell:
        row = active_cell['row']
        column_id = active_cell['column_id']
        value = booking_table.data[row][column_id]
        return [
            f'You clicked on row {row} and column "{column_id}", value: {value}',
            html.Div(id='input-container', children=[
                dcc.Input(id='input1', type='text', placeholder='Input 1'),
                dcc.Input(id='input2', type='text', placeholder='Input 2'),
                html.Button('Submit', id='submit-button')
            ])
        ]

@app.callback(
    Output('submit-output', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input1', 'value'),
     State('input2', 'value')]
)
def update_submit_output(n_clicks, input1, input2):
    if n_clicks:
        return f'Input 1: {input1}, Input 2: {input2}'

@app.callback(
    Output('booking-table', 'data'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_booking_table(start_date, end_date):
    df = pd.read_csv('test_data.csv')
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    df = df.set_index(df['date'])
    df = df.resample('D').first().fillna('FREE')
    df = df.reset_index()
    df['date'] = df['date'].dt.date

    if start_date and end_date:
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        df.loc[mask, 'name'] = 'TAKEN'

    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
