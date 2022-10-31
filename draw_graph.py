import plotly.express as px
import pandas as pd
import requests
import time

import sys
from urllib.parse import urljoin

if len(sys.argv) != 2:
    print("please provide prometheus api url as cli argument")
    sys.exit(1)

prometheus_api_url = sys.argv[1]


current_time = time.time()

one_hour_before = current_time - 1 * 60 * 60

if not prometheus_api_url.endswith("/"):
    prometheus_api_url += "/"

series_name = "prometheus_tsdb_head_series"

response = requests.get(urljoin(
    prometheus_api_url,
    "api/v1/query_range"
), params={
    "query": series_name,
    "start": int(one_hour_before),
    "end": int(current_time),
    "step": "15s"
})

if response.status_code != 200:
    print(f"prometheus endpoint returned HTTP {response.status_code}")
    sys.exit(1)

try:
    data = response.json()['data']['result'][0]['values']
except IndexError:
    print("failed to find metric in result json, check if metric name is valid")
    sys.exit(1)

time_scales, values = map(list, zip(*data))

df = pd.DataFrame(dict(
    time=pd.to_datetime(time_scales, unit='s', utc=True),
    values=values
))

graph = px.line(df, x=df['time'], y=df['values'], title=series_name)


with open("graph.png", 'wb') as f:

    f.write(graph.to_image())
