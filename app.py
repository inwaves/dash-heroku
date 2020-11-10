import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

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

# Dash initialisation
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# Dash init end

# Read DataFrame, generate plot
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

fig = px.bar(df, x="state", y="beef", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
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
    html.Label('Select state(s)'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['Alabama'],
        multi=True
    )]),

    dcc.Graph(
        id='agricultural-exports',
        figure=fig
    ),

    generate_table(df, 10)
])
# Generated app layout

if __name__ == '__main__':
    app.run_server(debug=True)