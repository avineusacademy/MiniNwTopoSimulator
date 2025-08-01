import networkx as nx
from pyvis.network import Network
from sqlmodel import Session, select
from models import Host, Switch

def build_topology():
    G = nx.Graph()
    with Session(engine) as sess:
        switches = sess.exec(select(Switch)).all()
        hosts = sess.exec(select(Host)).all()
    for sw in switches:
        G.add_node(sw.name, type="switch")
    for h in hosts:
        G.add_node(h.name, type="host")
        G.add_edge(h.name, f"Switch_{h.switch_id}")
    return G

def export_pyvis(G):
    net = Network(notebook=True)
    for n, attrs in G.nodes(data=True):
        shape = "square" if attrs["type"]=="switch" else "circle"
        net.add_node(n, label=n, shape=shape)
    for u,v in G.edges():
        net.add_edge(u, v)
    return net
