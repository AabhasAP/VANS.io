import requests
import subprocess
import socket

def fetch_crtsh(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        subdomains = set()
        for entry in data:
            name_value = entry.get("name_value", "")
            for sub in name_value.split("\n"):
                if sub.endswith(domain):
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        return [f"crt.sh error: {str(e)}"]

def fetch_gau(domain):
    try:
        result = subprocess.check_output(["gau", domain], timeout=10)
        urls = result.decode().splitlines()
        return list(set(urls))
    except subprocess.TimeoutExpired:
        return ["gau error: Request timed out."]
    except FileNotFoundError:
        return ["gau error: 'gau' is not installed or not in PATH."]
    except Exception as e:
        return [f"gau error: {str(e)}"]

def scan(domain: str):
    crtsh_results = fetch_crtsh(domain)
    gau_results = fetch_gau(domain)

    return {
        "crtsh": crtsh_results,
        "gau": gau_results
    }
def fetch_subfinder(domain):
    try:
        result = subprocess.run(["subfinder", "-d", domain, "-silent"], stdout=subprocess.PIPE, text=True, timeout=60)
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"subfinder error: {str(e)}"]

def fetch_amass(domain):
    try:
        result = subprocess.run(["amass", "enum", "-d", domain, "-nocolor", "-passive"], stdout=subprocess.PIPE, text=True, timeout=90)
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"amass error: {str(e)}"]

def resolve_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False

def dedupe_and_filter(subdomains, domain):
    cleaned = set()
    for sub in subdomains:
        sub = sub.strip().lower()
        if sub.endswith(domain) and re.match(r"^[a-zA-Z0-9.-]+$", sub):
            cleaned.add(sub)
    return sorted(cleaned)

def scan(domain):
    crtsh = fetch_crtsh(domain)
    gau = fetch_gau(domain)
    subfinder = fetch_subfinder(domain)
    amass = fetch_amass(domain)

    combined = crtsh + gau + subfinder + amass
    cleaned = dedupe_and_filter(combined, domain)

    resolved = [sub for sub in cleaned if resolve_domain(sub)]

    return {
        "resolved_subdomains": resolved,
        "unresolved_or_errors": list(set(cleaned) - set(resolved)),
        "source_breakdown": {
            "crtsh": crtsh,
            "gau": gau,
            "subfinder": subfinder,
            "amass": amass
        }
    }

