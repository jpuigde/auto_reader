import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from urllib.request import urlopen
#http://www.readingsoft.com/
WORDS_MINUTE = 200


def read_local():
    filename = 'text.txt'
    with open(filename, "r") as f:
        word_list = f.read().split()
    return word_list


def read_url(url):
    content = urlopen(url)
    word_list = []
    for line in content:
        word_list += str(line).split(' ')
    return word_list


def read_quijote():
    url = 'https://gist.githubusercontent.com/jsdario/6d6c69398cb0c73111e49f1218960f79/raw/8d4fc4548d437e2a7203a5aeeace5477f598827d/el_quijote.txt'
    return read_url(url)


def read_shakespeare():
    url = 'https://raw.githubusercontent.com/brunoklein99/deep-learning-notes/master/shakespeare.txt'
    return read_url(url)
# read_local()
# read_shakespeare()


TEXTS = {'Wiki': read_local,
         'Shakespeare': read_shakespeare,
         'Quijote': read_quijote
         }

word_list = read_local()

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        dcc.Dropdown(
            id='text-selected',
            options=[{'label': x, 'value': x}
                     for x in TEXTS],
            value='Wiki',
            clearable=False
        ),
        html.Center([html.H3(id='live-update-text', style={'align-items': 'center'})]),
        html.Button('Restart', id='reset_button'),
        html.Div(id='full-text'),
        dcc.Interval(
            id='interval-component',
            interval=60000/WORDS_MINUTE, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('full-text', 'children'),
              Input('text-selected', 'value'))
def update_text(name):
    global word_list
    word_list = TEXTS[name]()
    return ' '.join(word_list)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_word(n):
    return f'{word_list[n]}'


@app.callback(Output('interval-component', 'n_intervals'),
              [Input('reset_button', 'n_clicks')])
def reset_stream(reset):
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)
