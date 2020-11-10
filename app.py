import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# Dash initialisation
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# Dash init end

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# Read DataFrame, generate plot
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv',
                index_col=0)
# Read, generated plot end

md_intro = '''
## US states' agricultural exports 
You can filter which states are displayed using the first drop-down.
You can also control the type of plot using the second dropdown.
'''

# Generate app layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Title(children=['US agricultural exports']),

    dcc.Markdown(children=md_intro),

    html.Div(children=[
    html.Label('Select state(s):'),
    dcc.Dropdown(
        id='state-selector',
        options=[
            {'label': i, 'value': i} for i in df.index
        ],
        value=['Alabama'],
        multi=True
    ),

    html.Label('Select plot type:'),
    dcc.Dropdown(
        id='plot-type',
        options=[
            {'label': 'Bar plot', 'value': 'bar'},
            {'label': 'Line plot', 'value': 'line'},
            {'label': 'Scatter plot', 'value': 'scatter'}
        ],
        value=['bar']
    )
    ]),

    dcc.Graph(id='graph-with-filter'),

    generate_table(df, 10)
])


@app.callback(
    Output('graph-with-filter', 'figure'),
    [Input('state-selector', 'value'),
    Input('plot-type', 'value')])
def update_plot(states, plot_type):
    dff = df[df['state'] in states]

    # if plot_type == 'bar':
    fig = px.bar(dff, x="state", y="beef", barmode="group")
    # elif plot_type == 'line':
    #     fig = px.line(dff, x="state", y="beef")
    # elif plot_type == 'scatter':
    #     fig = px.scatter(dff, x="state", y="beef")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)