from dash import Dash, dcc, html
import plotly.graph_objects as go
from logging import getLogger

logger = getLogger(__name__)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash("Pixels", external_stylesheets=external_stylesheets)

# ! TODO !
# Read the data from the MysteryPicture table, and display it in a heatmap.
# The plotly heatmap expects a 500*500 matrix of integers
arr = []

heatmap = go.Heatmap(
    z=arr,
    colorscale='Greys_r',
    showscale=False
)

app.layout = html.Div(
    html.Div([
        html.H4("Who Am I?"),
        dcc.Graph(
            id="heatmap",
            figure={
                "data": [heatmap],
                "layout": go.Layout(
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, autorange="reversed"),
                    margin=dict(t=0, r=0, b=0, l=0),
                    width=500,
                    height=500,
                    autosize=False
                ),
            }
        )
    ])
)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081)
