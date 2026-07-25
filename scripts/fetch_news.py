"""
保険業界ニュースをGoogle News RSSから取得し、docs/news.json に保存するスクリプト。
GitHub Actionsから定期実行される。標準ライブラリのみ使用（pip install不要）。
"""
import html
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

QUERY = "保険業界 OR 生保 OR 損保"
RSS_URL = (
    "https://news.google.com/rss/search?q="
    + urllib.parse.quote(QUERY)
    + "&hl=ja&gl=JP&ceid=JP:ja"
)
OUTPUT_PATH = "docs/news.json"
MAX_ITEMS = 16


def strip_html(raw: str) -> str:
    """description内のHTMLタグを除去してプレーンテキスト化"""
    text = re.sub(r"<[^<]+?>", "", raw or "")
    return html.unescape(text).strip()


def fetch_rss(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; HokenNewsBot/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=20) as res:
        return res.read()


def parse_items(xml_bytes: bytes) -> list:
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        description = strip_html(item.findtext("description") or "")
        if title and link:
            items.append(
                {
                    "title": html.unescape(title),
                    "link": link,
                    "pubDate": pub_date,
                    "description": description,
                }
            )
    return items[:MAX_ITEMS]


def main():
    xml_bytes = fetch_rss(RSS_URL)
    items = parse_items(xml_bytes)

    payload = {
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(items)} items to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
