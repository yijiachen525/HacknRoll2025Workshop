from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly
import plotly.graph_objects as go
from logging import getLogger

from common.hockey import HockeyTeamResults

logger = getLogger(__name__)

TABLE_COLUMNS = ["TeamName",
                 "Year",
                 "Wins",
                 "Losses",
                 "OTLosses",
                 "WinPct",
                 "GoalsFor",
                 "GoalsAgainst",
                 "GoalsDifference",
                 ]

TABLE_CONFIG = {
    "page_size": 25,
    "filter_action": "native",
    "sort_action": "native",
    "columns": [{"name": i, "id": i} for i in TABLE_COLUMNS],
    "style_cell": {
        "whiteSpace": "normal",
        "height": "auto",
        "textAlign": "left",
        "fontFamily": "Arial",
        "fontSize": 14,
    },
    "style_header": {
        "backgroundColor": "rgb(230,230,230)",
        "fontWeight": "bold"
    },
    "style_data_conditional": [
        {
            "if": {"column_id": "Losses", "filter_query": "{Losses} > 40"},
            "backgroundColor": "rgba(255,0,0,0.5)",
            "color": "white"
        }
    ]
}

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash("HockeyTeamResults", external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.H4("Hockey Team Results"),
        html.Br(),
        dash_table.DataTable(id="complete-table", **TABLE_CONFIG),
        html.Br(),
        "Choose a team:",
        dcc.Dropdown(id="selected-team", persistence=True),
        dcc.Graph(id="team-time-series"),
        dcc.Interval(
            id="interval-component",
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        ),
        html.H4("Team with the highest Win Percentage each year"),
        dash_table.DataTable(id="win-pct-table", **TABLE_CONFIG),
    ])
)


@callback(Output("win-pct-table", "data"), Input("interval-component", "n_intervals"))
def update_data_table(n):
    logger.info("updating data table...")
    return HockeyTeamResults().get_win_pct_data()


@callback(Output("complete-table", "data"), Input("interval-component", "n_intervals"))
def update_data_table(n):
    logger.info("updating data table...")
    return HockeyTeamResults().get_all_data()


@callback(Output("selected-team", "options"), Input("interval-component", "n_intervals"))
def update_team_options(n):
    logger.info("updating teams...")
    data = HockeyTeamResults().get_all_data()
    return [result["TeamName"] for result in data]


@callback(
    Output("team-time-series", "figure"),
    Input("interval-component", "n_intervals"),
    Input("selected-team", "value"),
)
def update_graph_live(n, team: str):
    logger.info("updating graph...")
    data = HockeyTeamResults().get_all_data()
    team_data = [data_point for data_point in data if data_point["TeamName"] == team]

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=3, cols=2, vertical_spacing=0.2)
    fig["layout"]["margin"] = {
        "l": 30, "r": 10, "b": 30, "t": 10
    }
    fig["layout"]["legend"] = {"x": 0, "y": 1, "xanchor": "left"}

    for i, stat in enumerate(["Wins", "Losses", "OTLosses", "WinPct", "GoalsFor", "GoalsAgainst"]):
        col, row = divmod(i, 3)
        fig.append_trace({
            "x": [datapoint["Year"] for datapoint in team_data],
            "y": [datapoint[stat] for datapoint in team_data],
            "name": stat,
            "mode": "lines+markers",
            "type": "scatter"
        }, row + 1, col + 1)

    fig.update_layout(
        legend=dict(
            xanchor="center",
            y=1.1,
            x=0.5,
            orientation="h"
        )
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
