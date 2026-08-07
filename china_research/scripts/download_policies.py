"""Download 7 Chinese policy documents from government websites."""

import time
import requests
from bs4 import BeautifulSoup
from config import POLICY_DOCUMENTS, DOWNLOADS_DIR

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

TIMEOUT = 30
MAX_RETRIES = 3


def extract_text(html: str, url: str) -> str:
    """Extract article text from Chinese government HTML pages."""
    soup = BeautifulSoup(html, "html.parser")

    # Try common content containers on Chinese gov sites
    selectors = [
        {"class_": "TRS_Editor"},
        {"class_": "pages_content"},
        {"class_": "article-content"},
        {"class_": "content"},
        {"id": "UCAP-CONTENT"},
        {"class_": "text_con"},
        {"class_": "article_con"},
        {"class_": "Section0"},
    ]

    for sel in selectors:
        content = soup.find("div", **sel)
        if content:
            # Get text, preserving paragraph breaks
            paragraphs = content.find_all(["p", "div", "h1", "h2", "h3", "h4"])
            if paragraphs:
                text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                if len(text) > 100:
                    return text

    # Fallback: try <body> minus scripts/nav/footer
    body = soup.find("body")
    if body:
        for tag in body.find_all(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = body.get_text(separator="\n", strip=True)
        # Remove excessive blank lines
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return "\n\n".join(lines)

    return soup.get_text(separator="\n", strip=True)


def download_document(doc: dict) -> bool:
    """Download and save a single policy document."""
    doc_id = doc["id"]
    slug = doc["slug"]
    url = doc["url"]
    title = doc["title"]

    print(f"[{doc_id}/7] Downloading: {title}")
    print(f"       URL: {url}")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)

            # Handle Chinese encoding
            if resp.apparent_encoding:
                resp.encoding = resp.apparent_encoding
            elif "charset=gb" in resp.headers.get("Content-Type", "").lower():
                resp.encoding = "gb2312"
            else:
                resp.encoding = "utf-8"

            if resp.status_code != 200:
                print(f"       Attempt {attempt}: HTTP {resp.status_code}")
                if attempt < MAX_RETRIES:
                    time.sleep(3)
                    continue
                print(f"       FAILED after {MAX_RETRIES} attempts")
                return False

            html = resp.text

            # Save raw HTML
            html_path = DOWNLOADS_DIR / f"{doc_id}_{slug}.html"
            html_path.write_text(html, encoding="utf-8")

            # Extract and save clean text
            text = extract_text(html, url)
            txt_path = DOWNLOADS_DIR / f"{doc_id}_{slug}.txt"
            txt_path.write_text(text, encoding="utf-8")

            char_count = len(text)
            chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
            print(f"       Saved: {char_count} chars ({chinese_chars} Chinese)")

            if chinese_chars < 50:
                print(f"       WARNING: Very few Chinese characters - may be an error page")

            return True

        except requests.exceptions.RequestException as e:
            print(f"       Attempt {attempt}: {type(e).__name__}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(3)

    print(f"       FAILED after {MAX_RETRIES} attempts")
    return False


def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print("=" * 60)
    print("Downloading 7 Chinese policy documents")
    print("=" * 60)

    results = []
    for doc in POLICY_DOCUMENTS:
        success = download_document(doc)
        results.append((doc["title"], success))
        time.sleep(2)  # Be polite to gov servers

    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    for title, success in results:
        status = "OK" if success else "FAILED"
        print(f"  [{status}] {title}")

    success_count = sum(1 for _, s in results if s)
    print(f"\n{success_count}/{len(results)} documents downloaded successfully")


if __name__ == "__main__":
    main()
