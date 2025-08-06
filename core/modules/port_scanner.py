import socket

def scan(domain, port_range=(1, 1024)):
    open_ports = []
    try:
        for port in range(port_range[0], port_range[1]+1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((domain, port))
                if result == 0:
                    open_ports.append(port)
    except Exception as e:
        return {"error": str(e)}

    return {
        "domain": domain,
        "open_ports": open_ports if open_ports else "No open ports found in the scanned range."
    }
