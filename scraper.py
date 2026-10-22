import json
import time
from collections import Counter
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {
    "User-Agent": "InternCircle-Student-Scraper/1.0 (+https://quotes.toscrape.com)"
}
JSON_OUTPUT_FILE = "quotes.json"
TXT_OUTPUT_FILE = "quotes.txt"

def scrape_quotes():
    """Scrapes all quotes across paginated results politely."""
    quotes = []
    url = BASE_URL + "/"
    page_count = 1

    print("Initiating polite web scraping sequence...")

    while url:
        print(f"Scraping page {page_count}: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Network or HTTP error encountered: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_elements = soup.select("div.quote")

        for q in quote_elements:
            text_el = q.select_one("span.text")
            author_el = q.select_one("small.author")
            tag_els = q.select("a.tag")

            # Safely extract text with None checks
            text = text_el.get_text(strip=True) if text_el else "N/A"
            author = author_el.get_text(strip=True) if author_el else "Unknown"
            tags = [t.get_text(strip=True) for t in tag_els] if tag_els else []

            quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        # Locate next page link
        next_button = soup.select_one("li.next a")
        if next_button and "href" in next_button.attrs:
            url = BASE_URL + next_button["href"]
            page_count += 1
            # Respect server resources with rate limiting
            time.sleep(1)
        else:
            url = None

    return quotes

def save_to_json(data, filename=JSON_OUTPUT_FILE):
    """Saves structured records to JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully exported JSON to {filename}")

def save_to_txt(data, filename=TXT_OUTPUT_FILE):
    """Saves human-readable records to plain text."""
    with open(filename, "w", encoding="utf-8") as f:
        for idx, item in enumerate(data, 1):
            f.write(f"Quote #{idx}\n")
            f.write(f"Text: {item['text']}\n")
            f.write(f"Author: {item['author']}\n")
            f.write(f"Tags: {', '.join(item['tags'])}\n")
            f.write("-" * 50 + "\n")
    print(f"Successfully exported readable text to {filename}")

def print_summary_report(data):
    """Calculates and outputs basic statistics about the collected dataset."""
    if not data:
        print("No records collected.")
        return

    authors = [item["author"] for item in data]
    all_tags = [tag for item in data for tag in item["tags"]]

    author_counts = Counter(authors)
    tag_counts = Counter(all_tags)

    most_common_author, author_freq = author_counts.most_common(1)[0]
    most_common_tag, tag_freq = tag_counts.most_common(1)[0]

    print("\n--- Scraping Summary Report ---")
    print(f"Total quotes collected: {len(data)}")
    print(f"Most quoted author: {most_common_author} ({author_freq} quotes)")
    print(f"Most common tag: '{most_common_tag}' ({tag_freq} occurrences)")