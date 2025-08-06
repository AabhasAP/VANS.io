from prometheus_client import start_http_server, Counter

scan_counter = Counter("artemis_scans", "Total scan requests")

def start_metrics():
    start_http_server(5000)
    scan_counter.inc()
