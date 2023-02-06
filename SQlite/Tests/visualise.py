# RUN USING `py visualise.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# Vscode debug does not work for some reason, despite name indeed == "__main__".

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import os
import servicesqlite as serv
import numpy as np
from dash.dependencies import Output, Input

app = Dash(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__)) # path python file is located in. Which is DIFFERENT to current working directory (where the python file is being run from).
# db = serv.DB(dir_path + "\\test3.db")
# a = db.get_dataframe()
# print(a)

db = serv.DB(dir_path + "\\servicesqlite.db")
prev_entry = [0, 0, 0, 0]
dbf = pd.DataFrame(columns=["timestamp", "car_speed", "temperature", "humidity"])
dbf.loc[len(dbf)] = prev_entry
db.write(prev_entry)
step=1

# fig2 = px.line(dbf, x="timestamp", y=["car_speed", "temperature", "humidity"])

app.layout = html.Div(children=[
    # html.H1(children='Hello Dash'),

    # html.Div(children='''
    #     Dash: A web application framework for your data.
    # '''),

    # dcc.Graph(
    #     id='live-graph',
    # ),
    dcc.Graph(
        id='live-graph',
    ),
    dcc.Graph(
        id='live-graph-2',
    ),
    # dcc.Graph(
    #     id='live-graph-2',
    # ),

    dcc.Interval(
        id = "graph-update",
        interval = 1000,
        n_intervals = 0
    )

])

@app.callback(
    [Output('live-graph', 'figure'), Output('live-graph-2', 'figure')], Input('graph-update', 'n_intervals')
)
def update_graph_scatter(n):
    a = np.random.randint(-step, step+1, size=4)
    a[0] = 1
    print(a)
    dbf.loc[len(dbf)] = dbf.loc[len(dbf) - 1] + a

    fig = px.line(dbf, x="timestamp", y=["car_speed", "temperature", "humidity"])

    return fig, fig

if __name__ == '__main__':
    app.run_server(debug=False)