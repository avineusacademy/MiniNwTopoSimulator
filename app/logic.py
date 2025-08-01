import ipaddress
from db import engine
from sqlmodel import Session, select
from models import Host, Switch, Router, RouteEntry, Packet

def validate_ips(packet: Packet):
    with Session(engine) as sess:
        hosts = sess.exec(select(Host)).all()
    # verify both hosts' IPs exist in hosts table and in same or known subnets
    ...

def arp_resolve(packet: Packet):
    # Broadcast ARP request to hosts on same VLAN, respond with MAC
    ...

def simulate(packet: Packet):
    log = []
    # 1. L3 subnet validation
    packet = validate_ips(packet)
    log.append("✅ Subnet validation passed")
    # 2. ARP
    packet = arp_resolve(packet, log)
    # 3. L2 forwarding via switch MAC table
    ...
    # 4. L3 routing via router table
    ...
    return log
