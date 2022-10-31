# Prometheus graph

This repo contains example code for drawing data provided by prometheus api

## Installation & running

Install dependencies with

```bash
pip install -r requirements.txt
```

and run script with Python 3:

```bash
python draw_script.py <url to prometheus instance>
```

Provided url is expected to point to base prometheus path (eg. if you open prometheus Graph at `some-address/graph`, pass `some-address` to the script).
