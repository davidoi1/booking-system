import dash.exceptions
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State
from dash.dependencies import Input, Output, State, ALL
from datetime import datetime, timedelta

from test import get_booking_table

booking_table = get_booking_table()

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Spain Booking'),
    html.Hr(),

    html.H2('Calendar'),

    html.Div([
        html.Label('Date: '),
        dcc.Input(id='date-input'),
        html.Br(),

        html.Label('Name: '),
        dcc.Input(id='name-input'),
        html.Br(),

        html.Label('Number of days: '),
        dcc.Input(id='days-input', type='number', value=1),
        html.Br(),

        html.Button('Submit', id='submit-btn')
    ], style={'padding-bottom': '30px'}),

    booking_table
])


@app.callback(
    Output('date-input', 'value'),
    Output('name-input', 'value'),
    Input('booking-table', 'active_cell'),
    State('booking-table', 'derived_virtual_data'),
    State('booking-table', 'page_size'),
    State('booking-table', 'page_current'),
)
def display_click_data(active_cell, data, page_size, page_current):
    if active_cell:
        if not page_current:
            page_current = 0

        print(active_cell, page_size, page_current)
        row_id = active_cell['row'] + page_current * page_size

        row_data = data[row_id]
        print(row_data)

        if row_data['name'] == 'FREE':
            row_data['name'] = ''

        return [
            row_data['date'],
            row_data['name']
        ]


@app.callback(
    Output('booking-table', 'data'),
    Input('submit-btn', 'n_clicks'),
    State('date-input', 'value'),
    State('name-input', 'value'),
    State('days-input', 'value'),
    State('booking-table', 'derived_virtual_data'),
)
def update_booking_table(clicks, date, name, days, data):
    if not clicks:
        return dash.exceptions.PreventUpdate

    print(clicks, date, name, days, data)

    df = pd.DataFrame(data)
    print(df)

    df['date'] = pd.to_datetime(df['date'])
    date = datetime.strptime(date, '%Y-%m-%d')

    for i in range(days):

        cur_date = date + timedelta(days=i)
        df.loc[df['date'] == cur_date, 'name'] = name
        print(df[df['date'] == date])

    df['date'] = df['date'].dt.date

    df.to_csv('test_data.csv', index=False)

    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
