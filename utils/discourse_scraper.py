import requests
import json
import time

DISCOURSE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = f"{DISCOURSE_URL}/c/courses/tds-kb/34"
TOPICS_API_URL = f"{CATEGORY_URL}.json"
OUTPUT_FILE = "data/discourse_posts.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Cookie": "_ga_QHXRKWW9HH=GS1.3.1729355855.1.0.1729355855.0.0.0; _ga=GA1.1.1072207099.1687449470; _fbp=fb.2.1735729272660.130809985349440143; _gcl_au=1.1.1616569687.1745945756; _ga_5HTJMW67XK=GS2.1.s1749907758$o88$g1$t1749907802$j16$l0$h0; _ga_08NPRH5L4M=GS2.1.s1749907758$o74$g1$t1749907834$j44$l0$h0; _t=la5XRShklN9gq5gQ1%2BxeNLNcoajm7rXaULMeaji4RAF34TqujLarNFDS88cYWKuPXtSxFyL25K56HwtXPchWjyfOwCHsixZUAiAUpHMAW%2FYv3vG4PYSWeqQH2ZQzzejl01NE0nIDSx5jTwZFyys9TIRSk3vks3AGf1HOk%2FSuQjD8OJjBJzQehth9cDWI4VLz3dEy4yavpzSalv8Tx3nwx13lsfvPNUqSbxTWaOYaQq2p7dtk6ZBwF90%2FfUa0lMXq4UTpAoa7do%2FANLKamU4ttVDptPU3wvh%2FpZ4svkAjdgAghrSK3j6V6wgX%2FbqdTKqV--LsgAEFP9pnP73e4w--4lfD5l8AAbeT0J17gXyyyw%3D%3D; _forum_session=0EO2Jj88F0iJGgihhfPh8TgQld8vCRvUSuRbz7Zm6JF2TXHHUS9Fm%2FsdIgfXHVwh2PotstHZJkKHfNZI096mdw2jhL85zv0QgjqP%2FB5%2F6iwYg7C0AGEVleoAR2VugV%2BkBYYC0cH1eLKvreY%2BI22kQPF5%2BXZaMY4z04%2BxbBaU9geYcNH%2FKiGTXrVD9J5zfTE2FAIwWqEZarm8IITmWQQzUy%2FI1mHtOipKV%2FHl25syttdu71BvxX8cGbsFwl9qqsuBcIaGlOPXgu3AA2wKOA7cGiUweKYyZyDwRR4KLQB8epcs8l7S1uTFrYzABAo9LpiLzwpnkkc6qLolXZPmcAKAIDYSPhS18SMw1PpvMznbAXBwy%2Bnyg8XcRGYVbV455qeJPLWJt1YsW4zK2kFeYP72z%2FnUL0%2BIG59Zeqqig2qcq8HdzCM6Y9VahbYDtTHS9dWbx3pHQosuqO5LAdUG30jJqpR6uBPtcvEgWtz%2BlZliH7ExXyIB0%2BvM07c9TTX3AFlZjQU2E86fdo05NFxsOH1xMtIdhzBa1a3SClRyhVSR--EZwMSv36z9FSNUPu--eXjWYjNYZ%2FXWtDZ00GL7Ow%3D%3D"
}


def fetch_topics():
    print("📡 Fetching topic list from Discourse...")
    res = requests.get(TOPICS_API_URL, headers=HEADERS)
    if res.status_code == 403:
        raise Exception("🚫 403 Forbidden — Login may be required.")
    res.raise_for_status()
    data = res.json()
    return data["topic_list"]["topics"]

def fetch_topic_details(topic_id):
    print(f"🔍 Fetching topic {topic_id}")
    url = f"{DISCOURSE_URL}/t/{topic_id}.json"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 403:
        print("❌ Skipped due to 403")
        return None
    res.raise_for_status()
    return res.json()

def main():
    topics = fetch_topics()
    posts = []

    for topic in topics:
        topic_data = fetch_topic_details(topic["id"])
        if topic_data:
            posts.append({
                "id": topic["id"],
                "title": topic["title"],
                "content": topic_data.get("post_stream", {}).get("posts", [{}])[0].get("cooked", ""),
                "url": f"{DISCOURSE_URL}/t/{topic['slug']}/{topic['id']}"
            })
        time.sleep(1)  # Avoid being rate-limited

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)
    print(f"✅ Saved {len(posts)} posts to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
