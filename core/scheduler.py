from celery import Celery
from modules import port_scanner

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def async_port_scan(domain):
    return port_scanner.scan(domain)
