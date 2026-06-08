#!/usr/bin/env python3
"""
youtube_to_blog.py (v3)
========================
3 YouTube URLs -> 1 bai Hugo Markdown chat luong cao
aiprofreelancer.com - Vincent Pham

Cach dung:
  python youtube_to_blog.py \
    --urls "https://youtu.be/AAA" "https://youtu.be/BBB" "https://youtu.be/CCC" \
    --keyword "notion ai review 2026" \
    --product "Notion AI" \
    --affiliate "https://notion.so/affiliate"
"""

import anthropic
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Thieu package. Chay: pip install youtube-transcript-api anthropic python-slugify")
    sys.exit(1)

try:
    from slugify import slugify
except ImportError:
    def slugify(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'[\s-]+', '-', text)
        return text.strip('-')

# CONFIG
AUTHOR        = "Vincent Pham"
SITE_BASE_URL = "https://aiprofreelancer.com"
OUTPUT_DIR    = Path("./output_posts")
MAX_CHARS     = 10000


def extract_video_id(url):
    patterns = [
        r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Khong tim thay video ID: {url}")


def get_transcript(video_id, index):
    """Tuong thich voi youtube-transcript-api v0.x va v1.x"""
    print(f"   Video {index}: {video_id}")
    try:
        # --- Thu v1.x API (moi) ---
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id)
        # v1.x tra ve object co the iterate duoc
        snippets = list(transcript_obj)
        full_text = " ".join([
            s.text if hasattr(s, 'text') else s.get('text', '')
            for s in snippets
        ])

        if len(full_text) > MAX_CHARS:
            full_text = full_text[:MAX_CHARS] + "... [truncated]"
        print(f"   OK: {len(full_text):,} ky tu")
        return full_text

    except Exception as e1:
        try:
            # --- Thu v0.x API (cu) ---
            result = YouTubeTranscriptApi.get_transcript(
                video_id, languages=['en', 'en-US', 'en-GB']
            )
            full_text = " ".join([item['text'] for item in result])
            if len(full_text) > MAX_CHARS:
                full_text = full_text[:MAX_CHARS] + "... [truncated]"
            print(f"   OK (v0 fallback): {len(full_text):,} ky tu")
            return full_text
        except Exception as e2:
            print(f"   Video {index}: Loi - {e2} - bo qua")
            return ""


def get_all_transcripts(urls):
    print(f"\nBuoc 1: Lay transcript tu {len(urls)} video...")
    transcripts = {}
    for i, url in enumerate(urls, 1):
        try:
            video_id = extract_video_id(url)
            text = get_transcript(video_id, i)
            if text:
                transcripts[f"Video {i} ({video_id})"] = text
        except ValueError as e:
            print(f"   {e}")

    if not transcripts:
        raise RuntimeError("Khong lay duoc transcript tu bat ky video nao!")

    print(f"OK: Lay duoc {len(transcripts)}/{len(urls)} transcripts")
    return transcripts


def cross_analyze_with_claude(client, transcripts, product):
    print(f"\nBuoc 2: Claude dang cross-analyze {len(transcripts)} nguon...")

    combined = ""
    for label, text in transcripts.items():
        combined += f"\n\n{'='*50}\n{label.upper()}\n{'='*50}\n{text}"

    prompt = f"""Analyze {len(transcripts)} YouTube review(s) of "{product}".

Cross-analyze all sources and extract:

## CONSENSUS FACTS
- Pricing (exact numbers)
- Performance data
- Key features confirmed

## PROS (agreed by multiple sources)

## CONS & REAL COMPLAINTS

## CONFLICTING OPINIONS (where reviewers disagree)

## UNIQUE INSIGHTS (important points from only 1 source)

## COMPETITOR COMPARISONS
| Competitor | How it compares |

## PRICING DETAILS

## RED FLAGS

Be specific. Skip generic praise.

TRANSCRIPTS:
{combined}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    analysis = message.content[0].text
    print(f"OK: {len(analysis):,} ky tu")
    return analysis


def generate_article_with_claude(client, analysis, keyword, product, affiliate_link, source_count):
    print(f"\nBuoc 3: Claude dang viet bai tu {source_count} nguon...")

    current_year = datetime.now().year
    month_year   = datetime.now().strftime("%B %Y")

    prompt = f"""You are an SEO affiliate copywriter for aiprofreelancer.com.
Author: {AUTHOR} - MMO practitioner, Vietnam. Writing for global freelancer audience.

TARGET KEYWORD: "{keyword}"
PRODUCT: {product}
AFFILIATE LINK: {affiliate_link}
YEAR: {current_year}
SOURCES: {source_count} independent YouTube reviews cross-analyzed

RESEARCH DATA:
{analysis}

Write a complete Hugo-ready blog post (minimum 1,800 words).

STRUCTURE:
# [H1: keyword + {current_year} + honest/worth it]

[150-word PAS opening: Pain > Agitate > Solution]
> **Bottom line:** [40-50 word featured snippet]
[Soft CTA link]

---
## Quick Verdict
[Summary table + Top 3 strengths]

---
## Who Is {product} For?

---
## Core Features: What Actually Matters
[3-4 H3 subsections - benefits not specs]

---
## Pricing Breakdown
[Full table + commentary]
[Mid CTA]

---
## Honest Pros and Cons
[REAL pros + REAL cons - not fake]

---
## How It Compares to Alternatives
[Comparison table]

---
## FAQ (5 purchase objection questions)

---
## Final Verdict
[2-3 sentences + rating X.X/5]
[Hard CTA x2]

---
*Based on {source_count} independent reviews. {AUTHOR} - aiprofreelancer.com | {month_year}*
*Disclosure: Affiliate links. Commission at no extra cost to you.*

RULES:
- Minimum 1,800 words
- Natural keyword density 1.5-2%
- Tone: honest freelancer NOT salesman
- Every Con must be REAL and specific
- OUTPUT ONLY THE ARTICLE"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    article_text = message.content[0].text
    title_match  = re.search(r'^#\s+(.+)$', article_text, re.MULTILINE)
    title        = title_match.group(1) if title_match else f"{product} Review {current_year}"

    print(f"OK: {len(article_text.split()):,} tu")
    return {"title": title, "content": article_text}


def build_front_matter(title, keyword, product, slug):
    now      = datetime.now()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S+07:00")
    tags     = [w for w in keyword.split() if len(w) > 3][:5]
    tags_str = ', '.join([f'"{t}"' for t in tags])

    return f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
draft: false
author: "{AUTHOR}"
slug: "{slug}"
categories: ["Reviews", "Affiliate Marketing"]
tags: [{tags_str}]
cover:
  image: "/images/{slug}.png"
  alt: "{title}"
schema:
  type: "Review"
  rating: "4.5"
  ratingCount: "1"
  author: "{AUTHOR}"
  product: "{product}"
toc: true
---

"""


def save_markdown(front_matter, content, slug):
    OUTPUT_DIR.mkdir(exist_ok=True)
    filepath = OUTPUT_DIR / f"{slug}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(content)
    print(f"\nDa luu: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description='3 YouTube Videos -> 1 Hugo Blog Post',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Vi du - 3 video:
  python youtube_to_blog.py ^
    --urls "https://youtu.be/AAA" "https://youtu.be/BBB" "https://youtu.be/CCC" ^
    --keyword "notion ai review 2026" ^
    --product "Notion AI" ^
    --affiliate "https://notion.so/affiliate"

Vi du - 1 video:
  python youtube_to_blog.py ^
    --urls "https://youtu.be/AAA" ^
    --keyword "ultahost vps review 2026" ^
    --product "UltaHost VPS" ^
    --affiliate "https://ultahost.com/#art52hz"
        """
    )
    parser.add_argument('--urls',      required=True, nargs='+', help='1-3 YouTube URLs')
    parser.add_argument('--keyword',   required=True,            help='Target SEO keyword')
    parser.add_argument('--product',   required=True,            help='Product name')
    parser.add_argument('--affiliate', required=True,            help='Affiliate link')
    parser.add_argument('--api-key',   default=None,             help='Claude API key')

    args = parser.parse_args()

    if len(args.urls) > 3:
        print("Toi da 3 URLs. Chi dung 3 URL dau.")
        args.urls = args.urls[:3]

    print("\n=== aiprofreelancer.com - YouTube to Blog v3 ===")
    print(f"    {len(args.urls)} video(s) -> 1 bai viet")
    print("=" * 48)

    client = anthropic.Anthropic(api_key=args.api_key)

    try:
        transcripts = get_all_transcripts(args.urls)
        analysis    = cross_analyze_with_claude(client, transcripts, args.product)
        result      = generate_article_with_claude(
            client, analysis, args.keyword,
            args.product, args.affiliate, len(transcripts)
        )

        slug         = slugify(args.keyword)
        front_matter = build_front_matter(result['title'], args.keyword, args.product, slug)
        filepath     = save_markdown(front_matter, result['content'], slug)

        print("\n=== HOAN THANH! ===")
        print(f"File  : {filepath}")
        print(f"URL   : {SITE_BASE_URL}/posts/{slug}/")
        print(f"Nguon : {len(transcripts)} video(s)")
        print(f"\nBuoc tiep theo:")
        print(f"  1. Copy {filepath.name} -> content/posts/")
        print(f"  2. Them anh: static/images/{slug}.png")
        print(f"  3. git add . && git commit -m 'Add {args.product} review' && git push")

    except Exception as e:
        print(f"\nLoi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
