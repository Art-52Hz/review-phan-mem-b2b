#!/usr/bin/env python3
"""
find_videos.py — Tu dong tim video YouTube tot nhat cho review
aiprofreelancer.com — MSIP Tool

Cach dung:
  python find_videos.py "murf ai review 2026"
  python find_videos.py "jasper ai review" --count 5
  python find_videos.py "elevenlabs vs murf" --type comparison

Tieu chi chon video tot:
  - Views > 5,000
  - Duration 5-25 phut (du sau, khong qua dai)
  - Co CC/transcript
  - Channel lien quan tech/AI/freelance
"""

import argparse
import json
import re
import sys

try:
    import requests
except ImportError:
    print("Thieu requests. Chay: pip install requests")
    sys.exit(1)

# ─── CONFIG ──────────────────────────────────────
MIN_VIEWS    = 5_000
MIN_SEC      = 300    # 5 phut
MAX_SEC      = 1_800  # 30 phut
TOP_N        = 3      # So video tra ve
# ─────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def parse_views(text: str) -> int:
    """'1.2M views' -> 1200000"""
    if not text:
        return 0
    text = text.lower().replace(",", "").replace(" views", "").strip()
    try:
        if "m" in text:
            return int(float(text.replace("m", "")) * 1_000_000)
        if "k" in text:
            return int(float(text.replace("k", "")) * 1_000)
        return int(re.sub(r"[^0-9]", "", text))
    except ValueError:
        return 0


def parse_duration(text: str) -> int:
    """'12:34' or '1:23:45' -> seconds"""
    if not text or text == "?":
        return 0
    parts = text.strip().split(":")
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except ValueError:
        pass
    return 0


def score_video(v: dict) -> float:
    """Cham diem video: cao hon = tot hon cho review."""
    score = 0.0
    views = parse_views(v.get("views", ""))
    secs  = parse_duration(v.get("duration", ""))

    # Views
    if views >= 100_000: score += 40
    elif views >= 50_000: score += 30
    elif views >= 20_000: score += 20
    elif views >= 10_000: score += 15
    elif views >= 5_000:  score += 8
    else:                 score -= 10  # penalty

    # Duration (8-20 phut la optimal)
    if 480 <= secs <= 1200:  score += 30
    elif 300 <= secs < 480:  score += 15
    elif 1200 < secs <= 1500: score += 10
    elif secs < 300:          score -= 20
    else:                     score += 5

    # Title keywords (review/honest/worth it = good)
    title_lower = v.get("title", "").lower()
    for kw in ["honest", "worth it", "review", "test", "2025", "2026", "vs"]:
        if kw in title_lower:
            score += 5

    # Avoid brand/promo channels
    avoid = ["official", "channel", "team", "inc", "corp", "hq", "labs official"]
    channel_lower = v.get("channel", "").lower()
    if any(a in channel_lower for a in avoid):
        score -= 15

    return score


def search_youtube(query: str, limit: int = 15) -> list:
    """Tim video tren YouTube. Chay tren may local, khong can API key."""
    url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Loi ket noi YouTube: {e}")
        return []

    # Extract ytInitialData JSON
    match = re.search(r"var ytInitialData\s*=\s*(\{.*?\});\s*</script>",
                      r.text, re.DOTALL)
    if not match:
        # Try alternate pattern
        match = re.search(r"ytInitialData\s*=\s*(\{.+?\});\s*(?:var |</script>)",
                          r.text, re.DOTALL)
    if not match:
        print("Khong parse duoc YouTube response. Thu lai sau.")
        return []

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        print("JSON parse error.")
        return []

    videos = []
    try:
        sections = (data["contents"]
                       ["twoColumnSearchResultsRenderer"]
                       ["primaryContents"]
                       ["sectionListRenderer"]
                       ["contents"])
        for section in sections:
            items = section.get("itemSectionRenderer", {}).get("contents", [])
            for item in items:
                if "videoRenderer" not in item:
                    continue
                v = item["videoRenderer"]
                vid = {
                    "id":       v.get("videoId", ""),
                    "title":    (v.get("title", {}).get("runs", [{}])[0]
                                  .get("text", "")),
                    "views":    (v.get("viewCountText", {})
                                  .get("simpleText", "0")),
                    "duration": (v.get("lengthText", {})
                                  .get("simpleText", "?")),
                    "channel":  (v.get("ownerText", {})
                                  .get("runs", [{}])[0].get("text", "")),
                }
                if vid["id"]:
                    videos.append(vid)
                if len(videos) >= limit:
                    break
            if len(videos) >= limit:
                break
    except (KeyError, IndexError):
        pass

    return videos


def filter_and_rank(videos: list) -> list:
    """Loc theo tieu chi + rank theo score."""
    filtered = []
    for v in videos:
        secs  = parse_duration(v.get("duration", ""))
        views = parse_views(v.get("views", ""))
        if secs < MIN_SEC or secs > MAX_SEC:
            continue
        if views < MIN_VIEWS:
            continue
        v["_score"] = score_video(v)
        v["_secs"]  = secs
        v["_views"] = views
        filtered.append(v)

    return sorted(filtered, key=lambda x: x["_score"], reverse=True)


def fmt_duration(secs: int) -> str:
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(
        description="Tim video YouTube tot nhat cho review — aiprofreelancer.com")
    parser.add_argument("keyword",        help='VD: "murf ai review 2026"')
    parser.add_argument("--count",  "-n", type=int, default=TOP_N,
                        help=f"So video tra ve (mac dinh {TOP_N})")
    parser.add_argument("--type",         default="review",
                        choices=["review", "comparison", "howto"],
                        help="Loai bai (anh huong tu khoa tim kiem)")
    args = parser.parse_args()

    # Mo rong tu khoa theo loai bai
    base = args.keyword
    if args.type == "comparison" and "vs" not in base.lower():
        queries = [base, base + " comparison", base + " vs alternative"]
    elif args.type == "howto":
        queries = [base, "how to use " + base, base + " tutorial"]
    else:
        queries = [base, base + " honest review", base + " worth it"]

    print(f"\n=== Tim video YouTube cho: '{base}' [{args.type}] ===")

    all_videos = {}
    for q in queries[:2]:
        print(f"   Search: {q}")
        found = search_youtube(q, limit=12)
        for v in found:
            if v["id"] not in all_videos:
                all_videos[v["id"]] = v
    
    if not all_videos:
        print("\nKhong tim duoc video. Co the YouTube dang block IP.")
        print("Thu: mo trinh duyet va tim tay tai youtube.com/results?search_query=...")
        return

    ranked = filter_and_rank(list(all_videos.values()))

    if not ranked:
        print(f"\nKhong co video nao qua tieu chi (views>{MIN_VIEWS:,}, duration {MIN_SEC//60}-{MAX_SEC//60} phut).")
        print("All videos found (unfiltered):")
        for v in list(all_videos.values())[:5]:
            print(f"  {v['id']} | {v['views']:>12} | {v['duration']:>7} | {v['title'][:50]}")
        return

    top = ranked[:args.count]

    print(f"\n{'='*60}")
    print(f"TOP {len(top)} VIDEO PHU HOP NHAT\n")
    urls = []
    for i, v in enumerate(top, 1):
        url = f"https://www.youtube.com/watch?v={v['id']}"
        urls.append(url)
        dur = fmt_duration(v["_secs"])
        views_k = f"{v['_views']//1000}K" if v['_views'] >= 1000 else str(v['_views'])
        print(f"[{i}] {views_k:>7} views | {dur:>7} | {v['channel'][:20]}")
        print(f"     {v['title'][:60]}")
        print(f"     {url}")
        print()

    # In luon lenh chay
    print("="*60)
    print("COPY LENH NAY DE CHAY LUON:\n")
    url_args = " ".join([f'"{u}"' for u in urls])
    print(f"python youtube_to_blog.py `")
    print(f"  --urls {url_args} `")
    print(f"  --keyword \"{base}\" `")
    print(f"  --product \"PRODUCT_NAME\" `")
    print(f"  --affiliate \"AFFILIATE_LINK\"")
    print()


if __name__ == "__main__":
    main()
