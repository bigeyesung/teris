import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def draw(bricks, space):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=bricks[:,0],
        y=bricks[:,1],
        marker=dict(color="red", size=12),
        mode="markers",
        name="bricks",
    ))

    fig.add_trace(go.Scatter(
        x=space[:,0],
        y=space[:,1],
        marker=dict(color=bricks, size=12),
        mode="markers",
        name="empty space",
    ))

    fig.update_layout(title="tetris game",
                    xaxis_title="xcoord",
                    yaxis_title="ycoord")

    # fig.show()
    fig.write_image("images/fig1.png")