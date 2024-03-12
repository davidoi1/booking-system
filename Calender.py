import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime

app = dash.Dash(__name__)

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
    html.Div(id='output-container-date-picker-range')
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

if __name__ == '__main__':
    app.run_server(debug=True)
