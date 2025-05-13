
import requests
import validators
import whois
from urllib.parse import urlparse
from datetime import datetime
import json

# Thay YOUR_API_KEY_HERE bằng API Key thật từ Google Safe Browsing
GOOGLE_SAFE_BROWSING_API_KEY = 'YOUR_API_KEY_HERE'

def check_google_safe_browsing(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    payload = {
        "client": {
            "clientId": "yourcompanyname",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(endpoint, json=payload)
        result = response.json()
        return "Unsafe" if result.get("matches") else "Safe"
    except Exception as e:
        return f"Error checking safety: {e}"

def get_domain_info(url):
    domain = urlparse(url).netloc
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (datetime.now() - creation_date).days if creation_date else None
        return {"domain": domain, "age_days": age, "status": "Valid"}
    except Exception:
        return {"domain": domain, "age_days": None, "status": "Unknown or Invalid"}

def analyze_url(url):
    if not validators.url(url):
        return {"error": "Invalid URL format."}

    safety = check_google_safe_browsing(url)
    domain_info = get_domain_info(url)

    return {
        "url": url,
        "safety": safety,
        "domain_info": domain_info
    }

if __name__ == "__main__":
    url_to_check = input("Nhập URL bạn muốn kiểm tra: ")
    result = analyze_url(url_to_check)
    print(json.dumps(result, indent=4))
