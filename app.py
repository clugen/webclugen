from dash import Dash, html, dcc, Input, State, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from pyclugen import clugen
import numpy as np
import random


external_stylesheets = [dbc.themes.FLATLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    html.H1(children='WebClugen', style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col(
            dbc.Container([
                dbc.Label('Number of clusters'),
                dbc.Input(id='num_clusters', debounce=True, value=4, type='number', min=1, max=30, step=1),
                dbc.Label('Number of points'),
                dbc.Input(id='num_points', debounce=True, value=500, type='number', min=1, max=50000, step=1),
                dbc.Label('Direction'),
                dbc.Row([
                    dbc.Col(dbc.Input(id='dir1', debounce=True, value=1, type='number', step=0.01)),
                    dbc.Col(dbc.Input(id='dir2', debounce=True, value=1, type='number', step=0.01)),
                ]),
                dbc.Label('Angle dispersion (radians)'),
                dbc.Input(id='angle_disp', debounce=True, value=0.1, type='number', min=0.0, max=np.pi, step=0.001),
                dbc.Label('Cluster separation'),
                dbc.Row([
                    dbc.Col(dbc.Input(id='csep1', debounce=True, value=10, type='number', min=0.0, step=0.01)),
                    dbc.Col(dbc.Input(id='csep2', debounce=True, value=10, type='number', min=0.0, step=0.01)),
                ]),
                dbc.Label('Line length'),
                dbc.Input(id='llength', debounce=True, value=6.0, type='number', min=0.0, max=np.iinfo(np.int32).max),
                dbc.Label('Line length dispersion'),
                dbc.Input(id='llength_disp', debounce=True, value=1.0, type='number', min=0, max=np.iinfo(np.int32).max),
                dbc.Label('Lateral dispersion'),
                dbc.Input(id='lateral_disp', debounce=True, value=1.0, type='number', min=0, max=np.iinfo(np.int32).max),
                dbc.Label('Empty clusters'),
                dbc.Switch(id='allow_empty', label='Allow?', value=False),
                dbc.Label('Cluster offset'),
                dbc.Row([
                    dbc.Col(dbc.Input(id='coff1', debounce=True, value=0, type='number', step=0.01)),
                    dbc.Col(dbc.Input(id='coff2', debounce=True, value=0, type='number', step=0.01)),
                ]),
                dbc.Label('Projection distribution'),
                dbc.Select(id="proj_dist_fn", options=[ {"label": "norm", "value": "norm"}, {"label": "unif", "value": "unif"} ], value="norm"),
                dbc.Label('Point distribution'),
                dbc.Select(id="point_dist_fn", options=[ {"label": "n-1", "value": "n-1"}, {"label": "n", "value": "n"} ], value="n-1"),
                dbc.Label('Seed'),
                dbc.Switch(id='auto_seed', label='Auto seed?', value=True),
                dbc.Input(id='seed', debounce=True, value=0, type='number', min=0, max=np.iinfo(np.int32).max, step=1),
                dbc.Button("Generate", id="gen-button", color="primary", className="me-1"),
            ]),
            width=3),
        dbc.Col(
            dbc.Container([
                dcc.Graph(id='plot', figure={}),
            ]),
            width=9
        ),
    ]),
])

# Add controls to build the interaction
@callback(
    Output('plot', 'figure'),
    Output('seed', 'value'),
    Input('gen-button', 'n_clicks'),
    State('num_clusters', 'value'),
    State('num_points', 'value'),
    State('dir1', 'value'),
    State('dir2', 'value'),
    State('angle_disp', 'value'),
    State('csep1', 'value'),
    State('csep2', 'value'),
    State('llength', 'value'),
    State('llength_disp', 'value'),
    State('lateral_disp', 'value'),
    State('allow_empty', 'value'),
    State('coff1', 'value'),
    State('coff2', 'value'),
    State('proj_dist_fn', 'value'),
    State('point_dist_fn', 'value'),
    State('auto_seed', 'value'),
    State('seed', 'value')
)
def update_plot(n_clicks, num_clusters, num_points, dir1, dir2, angle_disp, csep1, csep2,
        llength, llength_disp, lateral_disp, allow_empty, coff1, coff2, proj_dist_fn,
        point_dist_fn, auto_seed, seed):

    if auto_seed:
        seed = random.randrange(np.iinfo(np.int32).max)
    out2d = clugen(2, num_clusters, num_points, [dir1, dir2], angle_disp, [csep1, csep2], llength, llength_disp, lateral_disp,
        allow_empty=allow_empty, cluster_offset=[coff1, coff2], proj_dist_fn=proj_dist_fn, point_dist_fn=point_dist_fn, rng=seed)
    fig = px.scatter(x=out2d.points[:, 0], y=out2d.points[:, 1], color=out2d.clusters.astype(str))
    return [fig, seed]

@callback(
    Output('seed', 'disabled'),
    Input('auto_seed', 'value'),
)
def toggle_auto_seed(auto_seed):
    return auto_seed

if __name__ == '__main__':
    app.run(debug=True)