import streamlit as st
import requests
import streamlit.components.v1 as components
import time
import os

API_BASE = os.getenv("API_BASE", "http://backend:8000")


def wait_for_backend(url: str, retries: int = 10, delay: float = 1.0):
    for i in range(retries):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(delay)
    return False


# Wait for backend to be ready before anything else
if not wait_for_backend(f"{API_BASE}/health"):
    st.error("🚨 Backend not available. Please wait a few seconds and try again.")
    st.stop()

st.title("🌐 Mini Network Simulator (with topology & timeline)")

# Sidebar: define host A and B
ip_a = st.sidebar.text_input("Host A IP", "192.168.1.10")
ip_b = st.sidebar.text_input("Host B IP", "192.168.1.20")
vlan = st.sidebar.number_input("VLAN", 1, 4094, 10)


def format_step_text(step: str) -> str:
    if step.startswith("✅"):
        return f":green[✅ {step[1:].strip()}]"
    elif step.startswith("❌"):
        return f":red[❌ {step[1:].strip()}]"
    elif step.startswith("📦") or step.startswith("🔍") or step.startswith("📡"):
        return f":gray[⏳ {step[1:].strip()}]"
    else:
        return step


def run_simulation(src_ip, dst_ip, vlan):
    packet = {"src_ip": src_ip, "dst_ip": dst_ip, "vlan": vlan, "src_mac": None, "dst_mac": None}
    try:
        resp = requests.post(f"{API_BASE}/simulate", json=packet)
        if resp.status_code == 200:
            return resp.json()["log"]
        else:
            return [f"❌ Error: HTTP {resp.status_code}"]
    except requests.exceptions.ConnectionError:
        return ["❌ Error: Unable to connect to backend."]


def display_timeline(log: list[str]):
    st.subheader("📜 Simulation Timeline")
    for i, step in enumerate(log):
        formatted = format_step_text(step)
        st.markdown(f"**Step {i+1}:** {formatted}")
        time.sleep(0.8)

if st.button("Simulate Delivery"):
    log = run_simulation(ip_a, ip_b, vlan)
    display_timeline(log)

if st.button("Run Test Simulation"):
    st.info("Running automated test simulation...")
    log = run_simulation("192.168.1.10", "192.168.1.20", 10)
    display_timeline(log)

if st.button("Show Network Topology"):
    topo_html = requests.get(f"{API_BASE}/topology").text
    components.html(topo_html, height=400)
