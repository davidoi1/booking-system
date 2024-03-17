import dash.exceptions
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State
from dash.dependencies import Input, Output, State, ALL
from datetime import datetime, timedelta

# old way of getting booking table from csv file
#from test import get_booking_table
# booking_table = get_booking_table()

from sqlalchemy import create_engine, text
from db_credentials import db_connnection_string

def get_booking_table():
    engine = create_engine(db_connnection_string)
    booking_table_df = pd.read_sql('select * from booking_table', con=engine)

    booking_table_df['date'] = pd.to_datetime(booking_table_df['date'])
    current_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=180)
    booking_table_df.loc[len(booking_table_df.index)] = [current_datetime, None]

    booking_table_df = booking_table_df.set_index(booking_table_df['date'])
    booking_table_df = booking_table_df.drop(columns=['date'])

    booking_table_df = booking_table_df.resample('D').first().fillna('FREE')
    booking_table_df = booking_table_df.reset_index()

    booking_table_df['date'] = booking_table_df['date'].dt.date
    print(booking_table_df)

    # creating dash table
    table = dash_table.DataTable(
            id='booking-table',
            data=booking_table_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in booking_table_df.columns],
            page_size=60,
            style_data_conditional=[
                {
                    'if': {'column_id': 'name',
                           'filter_query': '{name} = "FREE"'},

                    'backgroundColor': 'green'
                }
            ]
        )

    return table

def sql_update(date, name):
    engine = create_engine(db_connnection_string)

    with engine.connect() as con:
        sql = text(f"REPLACE into booking_table (date, name) values (:date, :name)")
        params = {'name': name, 'date': date}

        con.execute(sql, parameters=params)

        con.commit()


table = get_booking_table()


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

    table
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
        cur_date = cur_date.date()
        sql_update(cur_date, name)

    # ToDo: rewrite into function
    engine = create_engine(db_connnection_string)
    booking_table_df = pd.read_sql('select * from booking_table', con=engine)

    booking_table_df['date'] = pd.to_datetime(booking_table_df['date'])
    current_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=180)
    booking_table_df.loc[len(booking_table_df.index)] = [current_datetime, None]

    booking_table_df = booking_table_df.set_index(booking_table_df['date'])
    booking_table_df = booking_table_df.drop(columns=['date'])

    booking_table_df = booking_table_df.resample('D').first().fillna('FREE')
    booking_table_df = booking_table_df.reset_index()

    booking_table_df['date'] = booking_table_df['date'].dt.date
    print(booking_table_df)

    return booking_table_df.to_dict('records')


if __name__ == '__main__':
    app.run_server()
