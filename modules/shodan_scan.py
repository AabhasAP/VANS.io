import shodan
from core.config import SHODAN_API_KEY

def scan(ip):
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        result = api.host(ip)
        return result
    except Exception as e:
        return {"error": str(e)}

