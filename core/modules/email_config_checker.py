import dns.resolver

def check_dns_record(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [r.to_text() for r in answers]
    except Exception as e:
        return [f"{record_type} error: {str(e)}"]

def scan(domain):
    results = {
        "MX": check_dns_record(domain, "MX"),
        "SPF": check_dns_record(f"_spf.{domain}", "TXT"),
        "DKIM": check_dns_record(f"selector._domainkey.{domain}", "TXT"),  # replace selector as needed
        "DMARC": check_dns_record(f"_dmarc.{domain}", "TXT"),
    }
    return results
