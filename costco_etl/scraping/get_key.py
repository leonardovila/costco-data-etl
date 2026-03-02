import re
import requests

URL = "https://www.costco.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/144.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def extract_api_key(html: str) -> str | None:
    match = re.search(r'\\"authentification_token\\":\\"([a-f0-9\-]+)\\"', html)
    return match.group(1) if match else None

def run_get_key():
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()

    html = response.text
    return extract_api_key(html)

if __name__ == "__main__":
    run_get_key()
