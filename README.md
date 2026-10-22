# Polite Web Scraper for Quotes

An ethical, modular web scraper built in Python using `requests` and `BeautifulSoup4` to harvest public quotes, authors, and classification tags.

## Data Source & Legality
- **Target URL**: [https://quotes.toscrape.com](https://quotes.toscrape.com)
- **Compliance**: This domain is specifically designed and hosted as an open sandbox for practicing web scraping techniques without violating privacy or copyrighted digital property.

## Scraping Politeness & Ethics Rules
1. **Descriptive User-Agent**: Every request carries a custom User-Agent identifying the client rather than relying on default scraper headers.
2. **Rate Limiting**: Enforced a minimum `1-second` sleep delay between consecutive page fetches (`time.sleep(1)`) to avoid server hammering.
3. **Graceful Failures**: Configured timeout handling (`timeout=10`) and HTTP status validation (`raise_for_status()`) to abort gracefully if connection drops.
4. **Defensive Parsing**: Validates the presence of elements prior to extracting text to avoid `AttributeError` exceptions when tags are missing.

## Outputs
- `quotes.json`: Clean, formatted array of records with `indent=2`.
- `quotes.txt`: Human-readable text report.

## Setup & Run
```bash
pip install requests beautifulsoup4
python scraper.py