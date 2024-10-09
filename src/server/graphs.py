# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import pandas as pd
import base64
from io import BytesIO

from server.db import retrieve_data

def default_graph():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

def graph_data(): 
    results = retrieve_data()
    results = [dict(row) for row in results]
    df = pd.DataFrame(results)
    df['timestamp_unix_epoch'] = pd.to_datetime(df['timestamp'], format='mixed').map(pd.Timestamp.timestamp)
    return df 

def easy_linegraph():
    df = graph_data()
    fig = Figure()
    ax = fig.subplots()
    ax.scatter(df.timestamp_unix_epoch, df.temperature)
    ax.set_xticks(ticks=df.timestamp_unix_epoch[0::20], labels=df.timestamp[0::20], minor=False, rotation=90) 
    ax.set_ylabel("Temperature C")
    ax.set_xlabel("Time")
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
