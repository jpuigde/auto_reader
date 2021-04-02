import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
from urllib.request import urlopen


def read_local():
    filename = 'data/text.txt'
    with open(filename, "r") as f:
        word_list = f.read().split()
    return word_list


def read_url(url, n=1000):
    content = urlopen(url)
    word_list = []
    for line in content:
        word_list += str(line.decode('utf-8')).split(' ')
    return word_list[:n]


def read_quijote():
    url = 'https://gist.githubusercontent.com/jsdario/6d6c69398cb0c73111e49f1218960f79/raw/8d4fc4548d437e2a7203a5aeeace5477f598827d/el_quijote.txt'
    return read_url(url)


def read_shakespeare():
    url = 'https://raw.githubusercontent.com/brunoklein99/deep-learning-notes/master/shakespeare.txt'
    return read_url(url)

WORDS_MINUTE = 200
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
        html.Center([html.H2(id='live-update-text', style={'align-items': 'center'})]),
        daq.Slider(id='slider-words-minute',
                   min=50, max=500, value=WORDS_MINUTE,  # http://www.readingsoft.com/
                   handleLabel={"showCurrentValue": True, "label": "VALUE"}, step=10),
        html.Button('Restart', id='reset_button'),
        # html.Div(id='current-text'),
        dcc.Markdown(id='current-text',style={'text-align': 'justify'}),
        html.Div(id='hidden-div', style={'display':'none'}),
        dcc.Interval(
            id='interval-component',
            interval=60000/WORDS_MINUTE, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('interval-component', 'interval'),
              Input('slider-words-minute', 'value'))
def update_words_minute(words_minute):
    return 60000 / words_minute


@app.callback(Output('hidden-div', 'children'),
              Input('text-selected', 'value'))
def update_text(name):
    global word_list
    word_list = TEXTS[name]()
    return ' '.join(word_list)


@app.callback(Output('current-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_word(n):
    global word_list
    pre_text = ' '.join(word_list[:n])
    marked_word = '**' + word_list[n] + '**'
    post_text = ' '.join(word_list[(n+1):])
    return pre_text + ' ' + marked_word + ' ' + post_text


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
