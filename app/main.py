from fastapi import FastAPI
from logic import simulate
from db import init_db
from models import Packet
from topology import build_topology, export_pyvis

app = FastAPI()
init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/simulate")
def endpoint(packet: Packet):
    log = simulate(packet)
    return {"log": log}

@app.get("/topology")
def topo():
    G = build_topology()
    net = export_pyvis(G)
    html = net.generate_html()
    return html
