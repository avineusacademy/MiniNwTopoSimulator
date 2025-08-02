import ipaddress
from sqlmodel import Session, select
from db import engine
from models import Host, Packet


def validate_ips(packet: Packet) -> tuple[Packet, list[str]]:
    logs = []
    with Session(engine) as sess:
        hosts = sess.exec(select(Host)).all()

    src_host = next((h for h in hosts if h.ip == packet.src_ip), None)
    dst_host = next((h for h in hosts if h.ip == packet.dst_ip), None)

    if not src_host or not dst_host:
        logs.append("❌ One or both IPs not found in network hosts database.")
        raise ValueError("Invalid source or destination IP")

    # Check subnet match
    try:
        src_net = ipaddress.ip_network(packet.src_ip + "/24", strict=False)
        dst_net = ipaddress.ip_network(packet.dst_ip + "/24", strict=False)
    except ValueError as e:
        logs.append(f"❌ IP format error: {e}")
        raise

    if src_net != dst_net:
        logs.append(f"❌ Source and destination are in different subnets: {src_net} ≠ {dst_net}")
        raise ValueError("Different subnets")

    # Check VLAN match
    if src_host.vlan != dst_host.vlan:
        logs.append(f"❌ VLAN mismatch: src VLAN {src_host.vlan}, dst VLAN {dst_host.vlan}")
        raise ValueError("VLAN mismatch")

    # Set source MAC
    packet.src_mac = src_host.mac

    logs.append("✅ Subnet and VLAN validation passed")
    return packet, logs


def arp_resolve(packet: Packet, log: list[str]) -> Packet:
    with Session(engine) as sess:
        # Simulate ARP broadcast
        result = sess.exec(select(Host).where(Host.ip == packet.dst_ip)).first()
        if result:
            packet.dst_mac = result.mac
            log.append(f"✅ ARP resolved: {packet.dst_ip} → {packet.dst_mac}")
        else:
            log.append("❌ ARP resolution failed — destination host not found")
            raise ValueError("ARP failed")
    return packet


def simulate(packet: Packet) -> list[str]:
    log = []

    try:
        packet, validate_log = validate_ips(packet)
        log.extend(validate_log)
    except Exception as e:
        log.append(f"❌ Validation error: {e}")
        return log

    try:
        packet = arp_resolve(packet, log)
    except Exception as e:
        log.append(f"❌ ARP error: {e}")
        return log

    # Future steps: switch forwarding, routing
    log.append("📦 Packet is ready for Layer 2 forwarding")
    # log.append("📡 Packet routed via R1 to next hop...")

    return log
