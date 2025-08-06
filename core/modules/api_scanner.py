import requests
from urllib.parse import urljoin

def scan_api(base_url: str) -> dict:
    """
    Basic API scanner that checks for:
    - Open endpoints
    - CORS headers
    - HTTP method support
    """

    endpoints = ["/", "/api", "/status", "/login", "/health", "/v1", "/admin"]
    methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    results = {}

    for endpoint in endpoints:
        full_url = urljoin(base_url, endpoint)
        results[full_url] = {}
        try:
            for method in methods:
                resp = requests.request(method, full_url, timeout=5)
                results[full_url][method] = {
                    "status": resp.status_code,
                    "cors": resp.headers.get("Access-Control-Allow-Origin", "None"),
                    "content_type": resp.headers.get("Content-Type", "Unknown")
                }
        except requests.RequestException as e:
            results[full_url] = {"error": str(e)}

    return results
