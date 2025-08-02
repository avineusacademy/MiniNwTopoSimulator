from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Host(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ip: str
    mac: str
    vlan: int
    switch_id: int

class Switch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class VLAN(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vlan_id: int
    switch_id: int

class Router(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class RouteEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    router_id: int
    dst_subnet: str
    next_hop_ip: str

# Pydantic model for API payload
class Packet(BaseModel):
    src_ip: str
    dst_ip: str
    vlan: int
    src_mac: Optional[str] = None
    dst_mac: Optional[str] = None
