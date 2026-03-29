"""Capture screenshots of Chinese government websites using Playwright."""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from config import SCREENSHOT_TARGETS, SCREENSHOTS_DIR


def create_placeholder(name: str, url: str, filepath: Path):
    """Create a placeholder image when screenshot capture fails."""
    img = Image.new("RGB", (1280, 800), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        small_font = font

    draw.text((100, 300), f"Screenshot: {name}", fill=(80, 80, 80), font=font)
    draw.text((100, 360), f"URL: {url}", fill=(120, 120, 120), font=small_font)
    draw.text((100, 400), "(Could not capture live screenshot)", fill=(160, 160, 160), font=small_font)
    draw.rectangle([50, 50, 1230, 750], outline=(200, 200, 200), width=2)
    img.save(filepath)
    print(f"    Created placeholder: {filepath.name}")


def capture_screenshots():
    """Capture all screenshots using Playwright."""
    print("=" * 60)
    print("Capturing website screenshots")
    print("=" * 60)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: pip install playwright && python -m playwright install chromium")
        sys.exit(1)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="zh-CN",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        )

        for target in SCREENSHOT_TARGETS:
            name = target["name"]
            url = target["url"]
            filepath = SCREENSHOTS_DIR / f"{name}.png"

            print(f"\n  [{name}] {url}")

            try:
                page = context.new_page()
                page.goto(url, timeout=60000, wait_until="networkidle")
                page.wait_for_timeout(2000)  # Extra settle time
                page.screenshot(path=str(filepath), full_page=False)
                page.close()

                size_kb = filepath.stat().st_size / 1024
                print(f"    Captured: {filepath.name} ({size_kb:.0f} KB)")
                results.append((name, True))

            except Exception as e:
                print(f"    Failed: {e}")
                create_placeholder(name, url, filepath)
                results.append((name, False))
                try:
                    page.close()
                except Exception:
                    pass

        browser.close()

    print("\n" + "=" * 60)
    print("Screenshot Summary")
    print("=" * 60)
    for name, success in results:
        status = "OK" if success else "PLACEHOLDER"
        print(f"  [{status}] {name}")

    live_count = sum(1 for _, s in results if s)
    print(f"\n{live_count}/{len(results)} live screenshots captured")


if __name__ == "__main__":
    capture_screenshots()
