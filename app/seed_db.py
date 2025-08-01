from sqlmodel import Session
from db import engine, init_db
from models import Host, Switch, VLAN, Router, RouteEntry

def seed():
    init_db()
    with Session(engine) as session:
        # Add Switch
        sw1 = Switch(name="S1")
        session.add(sw1)
        session.commit()

        # Add VLAN
        vlan10 = VLAN(vlan_id=10, switch_id=sw1.id)
        session.add(vlan10)

        # Add Hosts
        h1 = Host(name="HostA", ip="192.168.1.10", mac="AA:BB:CC:DD:01", vlan=10, switch_id=sw1.id)
        h2 = Host(name="HostB", ip="192.168.1.20", mac="AA:BB:CC:DD:02", vlan=10, switch_id=sw1.id)
        session.add(h1)
        session.add(h2)

        # Add Router and routing
        r1 = Router(name="R1")
        session.add(r1)
        session.commit()
        route = RouteEntry(router_id=r1.id, dst_subnet="192.168.1.0/24", next_hop_ip="192.168.1.1")
        session.add(route)

        session.commit()
        print("✅ Seeded database with sample data.")

if __name__ == "__main__":
    seed()
