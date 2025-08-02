from fastapi import FastAPI
from logic import simulate
from db import init_db
from models import Packet
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi import APIRouter

# Use absolute import here (adjust if your setup requires)
from topology import build_topology, export_pyvis

app = FastAPI()
init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/simulate")
def endpoint(packet: Packet):
    try:
        log = simulate(packet)
        return {"log": log}
    except Exception as e:
        print(f"[simulate ERROR] {e}")
        return JSONResponse(status_code=500, content={"log": [f"Internal error: {str(e)}"]})

router = APIRouter()

@router.get("/topology", response_class=HTMLResponse)
def get_topology():
    G = build_topology()
    net = export_pyvis(G)

    # Save HTML for debugging
    html_content = net.generate_html()
    with open("debug_topology.html", "w") as f:
        f.write(html_content)
    return HTMLResponse(html_content)

# Include the router
app.include_router(router)

