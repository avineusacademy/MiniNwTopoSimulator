import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_simulate_valid_packet():
    packet = {
        "src_ip": "192.168.1.10",
        "dst_ip": "192.168.1.20",
        "vlan": 10
    }
    response = client.post("/simulate", json=packet)
    assert response.status_code == 200
    json_data = response.json()
    assert "log" in json_data
    assert any("Subnet validation" in step for step in json_data["log"])
    assert any("ARP" in step for step in json_data["log"])
