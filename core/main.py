from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from core.modules import (
    subdomain_scanner,
    port_scanner,
    shodan_scan,
    email_config_checker,
    api_scanner
)
from core.prometheus_metrics import start_metrics

app = FastAPI(title="🛡 VANS API", version="1.0")

@app.on_event("startup")
def startup_event():
    start_metrics()

# -----------------------------
# API ROUTES
# -----------------------------

@app.get("/api/")
def read_root():
    return {"message": "🛡 VANS API is running"}

@app.get("/api/scan/subdomains")
def scan_subdomains(domain: str):
    return subdomain_scanner.scan(domain)

@app.get("/api/scan/ports")
def scan_ports(domain: str):
    return port_scanner.scan(domain)

@app.get("/api/scan/shodan")
def scan_shodan(ip: str):
    return shodan_scan.scan(ip)

@app.get("/api/scan/email")
def scan_email_config(domain: str):
    return email_config_checker.scan(domain)

@app.get("/api/scan/api")
def scan_api_endpoint(url: str):
    return api_scanner.scan_api(url)

# -----------------------------
# REACT FRONTEND STATIC ROUTES
# -----------------------------

# Path to built frontend (copied via Docker)
frontend_path = Path(__file__).parent.parent / "core" / "static"
index_file = frontend_path / "index.html"

# Mount static assets
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if index_file.exists():
            return FileResponse(index_file)
        return {"detail": "Frontend not built or missing"}
