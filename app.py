from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
from pyclugen import clugen
import numpy as np


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='WebClugen', style={'textAlign':'center'}),
    dcc.Input(id='seed', placeholder='Enter seed...', type='number', min=0, max=np.iinfo(np.int32).max, step=1),
    dcc.Graph(id='plot', figure={})
])

# Add controls to build the interaction
@callback(
    Output(component_id='plot', component_property='figure'),
    Input(component_id='seed', component_property='value')
)
def update_graph(seed):
    out2d = clugen(2, 4, 400, [1, 0], 0.4, [50, 10], 20, 1, 2, rng=seed)
    fig = px.scatter(x=out2d.points[:, 0], y=out2d.points[:, 1], color=out2d.clusters.astype(str))
    return fig

if __name__ == '__main__':
    app.run(debug=True)