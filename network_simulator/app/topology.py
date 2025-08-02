import networkx as nx
from pyvis.network import Network
from sqlmodel import Session, select
from models import Host, Switch
from db import engine

def build_topology():
    G = nx.Graph()
    with Session(engine) as sess:
        switches = sess.exec(select(Switch)).all()
        hosts = sess.exec(select(Host)).all()

    # Create a mapping from switch_id to switch name
    switch_map = {sw.id: sw.name for sw in switches}

    for sw in switches:
        G.add_node(sw.name, type="switch")

    for h in hosts:
        G.add_node(h.name, type="host")
        if h.switch_id in switch_map:
            G.add_edge(h.name, switch_map[h.switch_id])
        else:
            print(f"Warning: switch_id {h.switch_id} not found for host {h.name}")

    return G

def export_pyvis(G):
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")
    for n, attrs in G.nodes(data=True):
        shape = "square" if attrs["type"] == "switch" else "dot"
        color = "skyblue" if attrs["type"] == "host" else "orange"
        net.add_node(n, label=n, shape=shape, color=color)
    for u, v in G.edges():
        net.add_edge(u, v)
    net.toggle_physics(True)
    return net