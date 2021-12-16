import plotly.express as px
from plotly.offline import plot
import pandas as pd

data = pd.read_json("audiobooks.json")
data["book"] = data["Path"].str.split("/").str[0]

audiodata = data[data["MimeType"].str.contains("audio")]

audiobooks = (
    audiodata.groupby("book").agg({"Size": ["count", "sum"], "ModTime": ["max"]})
).reset_index()

audiobooks.columns = ["book", "file_count", "sum", "timestamp"]

MB_SIZE = 1e6
audiobooks["size_h"] = audiobooks["sum"] / MB_SIZE
audiobooks["timestamp"] = pd.to_datetime(audiobooks["timestamp"])

cumulative = (
    audiobooks.sort_values("timestamp")
    .set_index("timestamp")["sum"]
    .cumsum()
    .to_frame()
    .reset_index()
    .reset_index()
    .rename(columns={"sum": "total_size", "index": "count"})
    .assign(size_mb=lambda x: x["total_size"] / 1e6)
).drop(columns=["total_size"])

fig = px.line(
    cumulative,
    x="timestamp",
    y="size_mb",
    title="Total Size in MB over Time",
    template="presentation",
)

plot(fig, filename="time_plot.html", show_link=True)

audiobooks.round(2).to_csv("audiobooks.csv")
