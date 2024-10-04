from matplotlib.ticker import LogLocator
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import base64
from io import BytesIO
from matplotlib.figure import Figure

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
    return df 


def easy_linegraph():
    df = graph_data()
    fig = Figure()
    ax = fig.subplots()
    ax.plot(df.timestamp, df.temperature)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

