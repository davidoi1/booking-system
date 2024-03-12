import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

number_buttons = [html.Button(str(i), id=f'number-{i}') for i in range(10)]
operation_buttons = [html.Button(op, id=f'operation-{op}') for op in ['+', '-', '*', '/']]
equal_button = html.Button('=', id='equal')
clear_button = html.Button('C', id='clear')

app.layout = html.Div([
    html.Div(number_buttons),
    html.Div(operation_buttons),
    equal_button,
    clear_button,
    html.Div(id='output'),
    html.Div(id='result-output'),  # New output window for the result
    dcc.Store(id='store', data='')
])

@app.callback(
    Output('store', 'data'),
    [Input(f'number-{i}', 'n_clicks') for i in range(10)] +
    [Input(f'operation-{op}', 'n_clicks') for op in ['+', '-', '*', '/']] +
    [Input('equal', 'n_clicks'),
     Input('clear', 'n_clicks')],  # Include clear button in the inputs
    [State('store', 'data')]
)
def update_store(*args):
    store_data = args[-1]
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'equal':
        try:
            store_data = str(eval(store_data))
        except Exception:
            store_data = 'Error'
    elif button_id == 'clear':
        store_data = ''
    elif button_id != 'store':
        value = button_id.split('-')[1]
        if button_id.startswith('operation') and store_data and store_data[-1] in ['+', '*', '/']:
            store_data = store_data[:-1] + value
        elif button_id == 'operation--':
            store_data += '-'
        else:
            store_data += value
    return store_data

@app.callback(
    Output('output', 'children'),
    [Input('store', 'data')]
)
def display_output(store_data):
    return store_data

@app.callback(
    Output('result-output', 'children'),  # Update the result output window
    [Input('equal', 'n_clicks')],
    [State('store', 'data')]
)
def display_result(equal_clicks, store_data):
    if equal_clicks is not None and equal_clicks > 0:
        try:
            result = str(eval(store_data))
        except Exception:
            result = 'Error'
        return f'Result: {result}'
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
