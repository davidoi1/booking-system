import pandas as pd
from datetime import datetime, timedelta
from dash import dash_table


def get_booking_table():
    df = pd.read_csv('test_data.csv')
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    current_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=270)
    df.loc[len(df.index)] = [current_datetime, None]

    df = df.set_index(df['date'])
    df = df.drop(columns=['date'])

    print(df)

    df = df.resample('D').first().fillna('FREE')
    df = df.reset_index()

    df['date'] = df['date'].dt.date

    print(df)

    table = dash_table.DataTable(
        id='booking-table',
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
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


if __name__ == '__main__':
    get_booking_table()
