from dash import Dash, html, dcc
import plotly.express as px
from pyclugen import clugen

out2d = clugen(2, 4, 400, [1, 0], 0.4, [50, 10], 20, 1, 2)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='WebClugen', style={'textAlign':'center'}),
    dcc.Graph(figure=px.scatter(x=out2d.points[:, 0], y=out2d.points[:, 1], color=out2d.clusters.astype(str)))
])

if __name__ == '__main__':
    app.run(debug=True)