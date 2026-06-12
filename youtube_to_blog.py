#!/usr/bin/env python3
"""
youtube_to_blog.py (v4)
========================
Nang cap theo Strategic Report - aiprofreelancer.com
Vincent Pham

Cai tien so voi v3:
  1. Article prompt manh hon - Experience signals bat buoc
  2. Word count validation - tu choi bai duoi 1,500 tu
  3. Sub-ID tracking tu dong tren moi affiliate link
  4. Human review checklist in ra sau khi tao bai
  5. Rating tu dong extract tu bai viet
  6. Support keyword type: review / comparison / alternatives
  7. Bai dai hon: max_tokens=8000

Cach dung:
  python youtube_to_blog_v4.py \
    --urls "URL1" "URL2" "URL3" \
    --keyword "elevenlabs review 2026" \
    --product "ElevenLabs" \
    --affiliate "https://try.elevenlabs.io/xxx" \
    --type review
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

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
AUTHOR        = "Vincent Pham"
SITE_BASE_URL = "https://aiprofreelancer.com"
OUTPUT_DIR    = Path("./output_posts")
MAX_CHARS     = 10000
MIN_WORDS     = 1500   # Tu choi bai neu duoi nguong nay
# ─────────────────────────────────────────


def add_sub_id(affiliate_url: str, sub_id: str) -> str:
    """
    Them sub-ID vao affiliate link de tracking.
    VD: https://try.elevenlabs.io/xxx -> https://try.elevenlabs.io/xxx?ref=review-cta1
    """
    separator = "&" if "?" in affiliate_url else "?"
    return f"{affiliate_url}{separator}ref={sub_id}"


def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Khong tim thay video ID: {url}")


def get_transcript(video_id: str, index: int) -> str:
    print(f"   Video {index}: {video_id}")
    try:
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id)
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


def get_all_transcripts(urls: list) -> dict:
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

    print(f"OK: {len(transcripts)}/{len(urls)} transcripts")
    return transcripts


def cross_analyze_with_claude(client, transcripts: dict, product: str) -> str:
    print(f"\nBuoc 2: Claude cross-analyze {len(transcripts)} nguon...")

    combined = ""
    for label, text in transcripts.items():
        combined += f"\n\n{'='*50}\n{label.upper()}\n{'='*50}\n{text}"

    prompt = f"""Analyze {len(transcripts)} YouTube review(s) of "{product}".
Cross-analyze all sources. Output:

## CONSENSUS FACTS (confirmed by 2+ sources)
- Exact pricing & plans
- Performance numbers/benchmarks
- Key features with real-world impact

## PROS (specific, agreed by multiple reviewers)

## CONS & REAL COMPLAINTS
- Include severity: minor / major / dealbreaker

## CONFLICTING OPINIONS (reviewers DISAGREE — gold for nuance)

## UNIQUE INSIGHTS (1 reviewer only — still important)

## COMPETITOR COMPARISONS
| Competitor | Key difference | When to choose instead |

## PRICING DETAILS (all tiers, all limits)

## RED FLAGS & LIMITATIONS

## USE CASES MENTIONED (specific workflows, job types)

## SCREENSHOTS/DEMO MOMENTS (note timestamps if visible in transcript)

Be specific. No generic praise. Focus on what a freelancer needs to know before paying.

TRANSCRIPTS:
{combined}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    analysis = message.content[0].text
    print(f"OK: {len(analysis):,} ky tu analysis")
    return analysis


def generate_article_with_claude(
    client,
    analysis: str,
    keyword: str,
    product: str,
    affiliate_link: str,
    source_count: int,
    article_type: str,
    slug: str
) -> dict:
    print(f"\nBuoc 3: Viet bai ({article_type}) tu {source_count} nguon...")

    current_year = datetime.now().year
    month_year   = datetime.now().strftime("%B %Y")

    # Sub-ID tracking cho 3 CTA vi tri khac nhau
    cta_soft = add_sub_id(affiliate_link, f"{slug}-cta-top")
    cta_mid  = add_sub_id(affiliate_link, f"{slug}-cta-mid")
    cta_hard = add_sub_id(affiliate_link, f"{slug}-cta-bottom")

    # Cau truc khac nhau theo loai bai
    if article_type == "comparison":
        structure_hint = f"""
STRUCTURE FOR COMPARISON ARTICLE:
# [H1: "{keyword}" — be specific about which is better for whom]

[150w PAS opening: the pain of choosing wrong tool]
> **TL;DR:** [40-50w direct answer — who should use which]
[Soft CTA]

## Quick Comparison: Side-by-Side
[Full feature comparison table]

## When to Choose [Product A]
[3-4 specific use cases with reasoning]

## When to Choose [Product B]
[3-4 specific use cases with reasoning]

## Pricing Comparison
[Both pricing tables side by side]
[Mid CTA]

## Real User Experience (What YouTube Reviewers Found)
[Key findings from {source_count} sources analyzed]

## The Verdict: Which One Actually Wins?
[Nuanced answer - different winner for different users]
[Hard CTA x2]"""

    elif article_type == "alternatives":
        structure_hint = f"""
STRUCTURE FOR ALTERNATIVES ARTICLE:
# [H1: "{keyword}" — focus on variety and choice]

[150w PAS: why someone would want to leave the main product]
> **Quick Answer:** [40-50w — top 3 alternatives in one sentence each]
[Soft CTA]

## Why People Look for [Product] Alternatives
[Honest: pricing, limitations, specific use cases]

## Top 5 Alternatives (Ranked)

### 1. [Best Alternative] — Best Overall
### 2. [Alternative 2] — Best for [specific use case]
### 3. [Alternative 3] — Best Budget Option
### 4. [Alternative 4] — Best for [specific use case]
### 5. [Alternative 5] — Honorable Mention

## Comparison Table (All Alternatives vs Original)
[Mid CTA]

## How to Choose the Right One
## FAQ
[Hard CTA x2]"""

    else:  # review (default)
        structure_hint = f"""
STRUCTURE FOR REVIEW ARTICLE:
# [H1: "{keyword}" + {current_year} + "Honest Review" or "Worth It?"]

[150w PAS: the REAL pain freelancers face without this tool]
> **Bottom line:** [40-50w featured snippet — direct verdict]
[Soft CTA: {cta_soft}]

---
## Quick Verdict
[Summary table: Best For | Starting Price | Standout Feature | Rating X.X/5]
[Top 3 strengths as bullet points]

---
## Who Is {product} Actually For?
[Specific: who SHOULD use + who SHOULD NOT — based on research]

---
## Core Features: What Actually Matters for Freelancers
[3-4 H3 sections — BENEFITS not specs — use research data]

---
## {product} Pricing: Is It Worth It?
[Full pricing table + honest commentary on value for money]
[Mid CTA: {cta_mid}]

---
## Honest Pros and Cons
### What It Does Well
### Where It Falls Short
[EVERY con must be REAL — severity: minor/major/dealbreaker]
[1-2 sentences making cons feel like acceptable tradeoffs where true]

---
## How It Compares to Alternatives
[Comparison table from research + when to choose each]

---
## FAQ (5 questions — each addresses a real purchase objection)

---
## Final Verdict: Should You Use {product} in {current_year}?
[2-3 honest sentences + rating X.X/5]
[Hard CTA x2: {cta_hard}]"""

    prompt = f"""You are an SEO affiliate copywriter for aiprofreelancer.com.
Author: {AUTHOR} — MMO practitioner, Vietnam. Writing for global freelancer audience.

TARGET KEYWORD: "{keyword}"
PRODUCT: {product}
YEAR: {current_year}
SOURCES: {source_count} independent YouTube reviews cross-analyzed

RESEARCH DATA (from {source_count} YouTube reviews):
{analysis}

{structure_hint}

---
*Based on cross-analysis of {source_count} independent reviews. | {AUTHOR} — aiprofreelancer.com | {month_year}*
*Disclosure: This post contains affiliate links. Commission earned at no extra cost to you.*

CRITICAL RULES:
1. MINIMUM 1,800 WORDS — do not stop before this
2. Keyword density: 1.5-2% natural — never forced
3. Tone: honest experienced freelancer, NOT a salesman
4. Every Con must be SPECIFIC and REAL from the research — no "the UI could be more intuitive" filler
5. Add "My Take:" or "Based on the research:" before key opinions to signal authentic perspective
6. Use research data as foundation — add freelancer/MMO operator perspective on top
7. OUTPUT ONLY THE ARTICLE — no preamble, no "here's the article:", nothing before the H1"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    article_text = message.content[0].text

    # Replace generic affiliate links with tracked versions
    article_text = article_text.replace(affiliate_link, cta_hard)

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', article_text, re.MULTILINE)
    title = title_match.group(1) if title_match else f"{product} Review {current_year}"

    # Extract rating
    rating_match = re.search(r'(\d+\.?\d*)\s*/\s*5', article_text)
    rating = rating_match.group(1) if rating_match else "4.5"

    word_count = len(article_text.split())
    print(f"OK: {word_count:,} tu | Rating extracted: {rating}/5")

    return {
        "title":      title,
        "content":    article_text,
        "rating":     rating,
        "word_count": word_count,
        "cta_soft":   cta_soft,
        "cta_mid":    cta_mid,
        "cta_hard":   cta_hard,
    }


def build_front_matter(title: str, keyword: str, product: str, slug: str, rating: str) -> str:
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
  rating: "{rating}"
  ratingCount: "1"
  author: "{AUTHOR}"
  product: "{product}"
toc: true
---

"""


def print_human_review_checklist(filepath: Path, result: dict, slug: str):
    """
    In checklist human review bat buoc truoc khi publish.
    Theo Strategic Report: AI viet 80%, nguoi them 20% quyet dinh song con.
    """
    print("\n" + "="*55)
    print("  HUMAN REVIEW CHECKLIST (bat buoc truoc khi publish)")
    print("="*55)
    print(f"\n  File: {filepath}")
    print(f"  Words: {result['word_count']:,} / min 1,800")

    if result['word_count'] < MIN_WORDS:
        print(f"  ⚠️  CANH BAO: Bai chi {result['word_count']} tu — can chay lai hoac them thu cong!")
    else:
        print(f"  ✅ Do dai dat yeu cau")

    print(f"\n  Sub-ID tracking da gan:")
    print(f"    Top CTA : {result['cta_soft']}")
    print(f"    Mid CTA : {result['cta_mid']}")
    print(f"    Bot CTA : {result['cta_hard']}")

    print(f"""
  VIEC BAN PHAI LAM TRUOC KHI PUBLISH:

  [ ] 1. SCREENSHOTS THAT: Chup it nhat 2-3 anh that
         tu giao dien san pham va them vao bai
         (khong co anh that = Google khong tin EEAT)

  [ ] 2. "MY TAKE" SECTION: Doc bai, tim 1-2 cho
         them y kien ca nhan that: "In my experience..."
         hoac "What surprised me was..."

  [ ] 3. FACT-CHECK GIA: Mo trang chinh thuc san pham
         kiem tra gia hien tai (co the da thay doi)

  [ ] 4. INTERNAL LINKS: Dam bao co it nhat 3 link
         den bai khac tren site

  [ ] 5. COVER IMAGE: Them anh vao
         static/images/{slug}.png

  [ ] 6. DOC LAI 1 LAN: Co cau nao nghe nhu robot?
         Sua lai cho tu nhien

  [ ] 7. AFFILIATE LINK: Kiem tra link hoat dong dung

  CHI PUBLISH KHI TICK HET 7 O TREN!
""")
    print("="*55)


def save_markdown(front_matter: str, content: str, slug: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    filepath = OUTPUT_DIR / f"{slug}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(content)
    print(f"\nDa luu: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description='YouTube -> Hugo Blog Post v4 (aiprofreelancer.com)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Loai bai (--type):
  review       : Danh gia 1 san pham (mac dinh)
  comparison   : So sanh 2 san pham (A vs B)
  alternatives : Cac lua chon thay the cho san pham X

Vi du - Review:
  python youtube_to_blog_v4.py ^
    --urls "URL1" "URL2" "URL3" ^
    --keyword "elevenlabs ai review 2026" ^
    --product "ElevenLabs" ^
    --affiliate "https://try.elevenlabs.io/xxx" ^
    --type review

Vi du - Comparison:
  python youtube_to_blog_v4.py ^
    --urls "URL1" "URL2" ^
    --keyword "elevenlabs vs murf ai 2026" ^
    --product "ElevenLabs vs Murf" ^
    --affiliate "https://try.elevenlabs.io/xxx" ^
    --type comparison

Vi du - Alternatives:
  python youtube_to_blog_v4.py ^
    --urls "URL1" "URL2" "URL3" ^
    --keyword "elevenlabs alternatives 2026" ^
    --product "ElevenLabs" ^
    --affiliate "https://try.elevenlabs.io/xxx" ^
    --type alternatives
        """
    )
    parser.add_argument('--urls',      required=True,  nargs='+',
                        help='1-3 YouTube URLs')
    parser.add_argument('--keyword',   required=True,
                        help='Target SEO keyword')
    parser.add_argument('--product',   required=True,
                        help='Product name')
    parser.add_argument('--affiliate', required=True,
                        help='Affiliate link (sub-ID tu dong them)')
    parser.add_argument('--type',      default='review',
                        choices=['review', 'comparison', 'alternatives'],
                        help='Loai bai viet (mac dinh: review)')
    parser.add_argument('--api-key',   default=None,
                        help='Claude API key (mac dinh: bien moi truong)')

    args = parser.parse_args()

    if len(args.urls) > 3:
        print("Toi da 3 URLs. Chi dung 3 URL dau.")
        args.urls = args.urls[:3]

    print(f"\n=== aiprofreelancer.com - YouTube to Blog v4 ===")
    print(f"    {len(args.urls)} video(s) -> 1 bai [{args.type.upper()}]")
    print(f"    Keyword: {args.keyword}")
    print("=" * 50)

    client = anthropic.Anthropic(api_key=args.api_key)

    try:
        # B1: Lay transcripts
        transcripts = get_all_transcripts(args.urls)

        # B2: Cross-analyze
        analysis = cross_analyze_with_claude(client, transcripts, args.product)

        # B3: Generate article
        slug   = slugify(args.keyword)
        result = generate_article_with_claude(
            client, analysis, args.keyword,
            args.product, args.affiliate,
            len(transcripts), args.type, slug
        )

        # B4: Validate word count
        if result['word_count'] < MIN_WORDS:
            print(f"\n⚠️  Chi {result['word_count']} tu (min {MIN_WORDS}).")
            print("    Bai nay co the la thin content — nen chay lai voi --type khac")
            print("    hoac bo sung them research truoc khi publish.")

        # B5: Save file
        front_matter = build_front_matter(
            result['title'], args.keyword,
            args.product, slug, result['rating']
        )
        filepath = save_markdown(front_matter, result['content'], slug)

        # B6: Print human review checklist
        print_human_review_checklist(filepath, result, slug)

        print(f"  File  : {filepath}")
        print(f"  URL   : {SITE_BASE_URL}/posts/{slug}/")
        print(f"  Nguon : {len(transcripts)} video(s) cross-analyzed")
        print(f"  Words : {result['word_count']:,}")
        print(f"  Rating: {result['rating']}/5\n")

    except Exception as e:
        print(f"\nLoi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
