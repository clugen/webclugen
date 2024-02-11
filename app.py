from dash import Dash, html, dcc, Input, State, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from pyclugen import clugen
import numpy as np


external_stylesheets = [dbc.themes.FLATLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    html.H1(children='WebClugen', style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col(dbc.Container([
            dbc.Label('Number of clusters'),
            dbc.Input(id='num_clusters', debounce=True, value=4, type='number', min=1, max=30, step=1),
            dbc.Label('Number of points'),
            dbc.Input(id='num_points', debounce=True, value=500, type='number', min=1, max=50000, step=1),
            # dbc.Label('Direction'),
            # dbc.Label('Angle dispersion'),
            # dbc.Label('Cluster separation'),
            # dbc.Label('Line length'),
            # dbc.Label('Line length dispersion'),
            # dbc.Label('Lateral dispersion'),
            dbc.Label('Seed'),
            dbc.Input(id='seed', debounce=True, value=0, type='number', min=0, max=np.iinfo(np.int32).max, step=1),
            dbc.Button("Generate", id="gen-button", color="primary", className="me-1")
    ]), width=3),
        dbc.Col(
            dcc.Graph(id='plot', figure={}),
            width=9
        ),
    ]),
])

# Add controls to build the interaction
@callback(
    Output('plot', 'figure'),
    Input('gen-button', 'n_clicks'),
    State('num_clusters', 'value'),
    State('num_points', 'value'),
    State('seed', 'value')
)
def update_graph(n_clicks, num_clusters, num_points, seed):
    out2d = clugen(2, num_clusters, num_points, [1, 0], 0.4, [50, 10], 20, 1, 2, rng=seed)
    fig = px.scatter(x=out2d.points[:, 0], y=out2d.points[:, 1], color=out2d.clusters.astype(str))
    return fig

if __name__ == '__main__':
    app.run(debug=True)