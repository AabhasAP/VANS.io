from fastapi import FastAPI
from core.modules import (
    subdomain_scanner,
    port_scanner,
    shodan_scan,
    email_config_checker,
    api_scanner  # ✅ Added API scanner module
)
from core.prometheus_metrics import start_metrics

app = FastAPI(title="🛡 VANS API", version="1.0")

@app.on_event("startup")
def startup_event():
    start_metrics()

@app.get("/")
def read_root():
    return {"message": "🛡 VANS API is running"}

# 🕵️ Subdomain Scanner
@app.get("/scan/subdomains")
def scan_subdomains(domain: str):
    return subdomain_scanner.scan(domain)

# 🔍 Port Scanner
@app.get("/scan/ports")
def scan_ports(domain: str):
    return port_scanner.scan(domain)

# 🌐 Shodan Intelligence
@app.get("/scan/shodan")
def scan_shodan(ip: str):
    return shodan_scan.scan(ip)

# 📧 Email Configuration Checker
@app.get("/scan/email")
def scan_email_config(domain: str):
    return email_config_checker.scan(domain)

# 🔐 API Vulnerability Scanner
@app.get("/scan/api")
def scan_api_endpoint(url: str):
    return api_scanner.scan_api(url)
