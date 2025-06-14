import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://tds.s-anand.net"
NOTES = [
    "introduction", "project", "project-submission", "embedding",
    "search", "fastapi", "docker", "deployment", "rag", "rag-evaluation"
]
SAVE_DIR = "data/course_html"

os.makedirs(SAVE_DIR, exist_ok=True)

def extract_text_from_page(slug):
    print(f"🌐 Fetching: {slug}")
    url = f"{BASE_URL}/#/2025-01/{slug}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html5lib")

        title = slug.replace("-", " ").title()
        body = soup.get_text()

        content = f"# {title}\n\n{body}"
        save_path = os.path.join(SAVE_DIR, f"{slug}.md")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Saved: {save_path}")
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")

def main():
    for slug in NOTES:
        extract_text_from_page(slug)

if __name__ == "__main__":
    main()
