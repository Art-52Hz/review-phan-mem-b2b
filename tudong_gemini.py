import os
import subprocess
from datetime import datetime
import time
import requests
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 1. CẤU HÌNH HỆ THỐNG
# ==========================================
REPO_PATH = r"D:\projects\review-phan-mem-b2b"
POSTS_DIR = os.path.join(REPO_PATH, "content", "posts")
IMAGES_DIR = os.path.join(REPO_PATH, "static", "images")

# Claude API key — lưu trong claude_key.txt (không commit lên GitHub)
_key_file = os.path.join(REPO_PATH, "claude_key.txt")
if os.path.exists(_key_file):
    with open(_key_file) as _f:
        CLAUDE_API_KEY = _f.read().strip()
else:
    CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")

CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# ==========================================
# 2. DANH SÁCH BÀI VIẾT TỰ ĐỘNG
# ==========================================
ARTICLES = [
    {
        "keyword": "best Windows VPS hosting 2026",
        "title": "Best Windows VPS Hosting in 2026: Fast, Cheap & Reliable",
        "slug": "best-windows-vps-hosting-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "best VPS hosting for WordPress sites 2026",
        "title": "Best VPS Hosting for WordPress in 2026: Speed, Price & Reliability",
        "slug": "best-vps-for-wordpress-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "Hostinger VPS review 2026",
        "title": "Hostinger VPS Review 2026: Is It Worth It?",
        "slug": "hostinger-vps-review-2026",
        "affiliate_url": "https://www.hostinger.com/vn?REFERRALCODE=ACFTUNGSAAEO",
        "affiliate_name": "Hostinger",
    },
    {
        "keyword": "VPS vs shared hosting which is better 2026",
        "title": "VPS vs Shared Hosting in 2026: Which Should You Choose?",
        "slug": "vps-vs-shared-hosting-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "best cheap dedicated server 2026",
        "title": "Best Cheap Dedicated Servers in 2026: Performance Without the Price Tag",
        "slug": "best-cheap-dedicated-server-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "best VPS under 10 dollars per month 2026",
        "title": "Best VPS Under $10/Month in 2026: Top Picks for Every Use Case",
        "slug": "best-vps-under-10-dollars-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "unlimited bandwidth VPS hosting review 2026",
        "title": "Best Unlimited Bandwidth VPS Hosting in 2026",
        "slug": "best-unlimited-bandwidth-vps-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "managed WordPress VPS hosting 2026",
        "title": "Best Managed WordPress VPS Hosting in 2026: Hands-Off Power",
        "slug": "managed-wordpress-vps-hosting-2026",
        "affiliate_url": "https://www.hostinger.com/vn?REFERRALCODE=ACFTUNGSAAEO",
        "affiliate_name": "Hostinger",
    },
]

# ==========================================
# 3. TẠO ẢNH BÌA (Pillow — self-hosted)
# ==========================================
THEMES = {
    "vps":     ((15, 32, 80),  (30, 90, 200)),
    "hosting": ((10, 40, 70),  (20, 100, 160)),
    "ai":      ((40, 15, 80),  (100, 40, 180)),
    "writing": ((15, 60, 50),  (30, 140, 100)),
    "seo":     ((70, 40, 10),  (170, 100, 20)),
    "default": ((20, 20, 50),  (50, 80, 150)),
}

def _get_theme(slug, title):
    t = (slug + title).lower()
    if "vps" in t:     return THEMES["vps"]
    if "hosting" in t: return THEMES["hosting"]
    if "writing" in t or "copy" in t or "jasper" in t: return THEMES["writing"]
    if "seo" in t or "semrush" in t: return THEMES["seo"]
    if "ai" in t:      return THEMES["ai"]
    return THEMES["default"]

def _wrap(text, max_chars=30):
    words = text.split()
    lines, line = [], ""
    for w in words:
        if len(line) + len(w) + 1 <= max_chars:
            line = (line + " " + w).strip()
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def generate_cover_image(slug, title):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    out = os.path.join(IMAGES_DIR, f"{slug}.png")
    if os.path.exists(out):
        return f"/images/{slug}.png"  # đã có rồi

    W, H = 1200, 630
    c1, c2 = _get_theme(slug, title)
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img, "RGBA")

    # Gradient
    for y in range(H):
        t = (y / H) ** 2
        r = int(c1[0]*(1-t) + c2[0]*t)
        g = int(c1[1]*(1-t) + c2[1]*t)
        b = int(c1[2]*(1-t) + c2[2]*t)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    # Grid + circles
    for x in range(0, W, 120): draw.line([(x,0),(x,H)], fill=(255,255,255,12))
    for y in range(0, H, 120): draw.line([(0,y),(W,y)], fill=(255,255,255,12))
    cx, cy = W-100, -80
    for r in [280,220,160]: draw.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(255,255,255,18), width=2)
    draw.rectangle([0, H-6, W, H], fill=(255,255,255,60))

    try:
        font_t = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 68)
        font_d = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26)
    except:
        font_t = ImageFont.load_default()
        font_d = font_t

    lines = _wrap(title)
    line_h = 80
    start_y = (H - len(lines)*line_h)//2 - 30
    draw.rectangle([60, start_y-20, 160, start_y-14], fill=(255,255,255,150))
    for i, ln in enumerate(lines):
        y = start_y + i*line_h
        draw.text((62, y+4), ln, font=font_t, fill=(0,0,0,100))
        draw.text((60, y),   ln, font=font_t, fill=(255,255,255,255))
    draw.text((60, H-52), "aiprofreelancer.com", font=font_d, fill=(255,255,255,180))

    img.save(out, "PNG", optimize=True)
    print(f"    [+] Đã tạo ảnh bìa: {slug}.png")
    return f"/images/{slug}.png"

# ==========================================
# 4. SINH NỘI DUNG BẰNG CLAUDE API
# ==========================================
def generate_content_with_claude(keyword, title, affiliate_url, affiliate_name):
    prompt = f"""Act as a Senior Technical SEO Expert and Expert Copywriter with 10+ years of experience. Write an extremely comprehensive, SEO-optimized blog post in English. Current year is 2026.

Keyword to rank for: '{keyword}'
Post Title: {title}

SEO & FORMATTING RULES:
1. Include '{keyword}' naturally in the FIRST 100 words, in at least one H2, one H3, and the conclusion.
2. MAXIMUM 3 sentences per paragraph. Bold important metrics. Use bullet points frequently.
3. Minimum 1,200 words.

STRUCTURE:
1. Introduction (150 words) — Hook + first affiliate CTA.
2. Key Factors to Consider (200 words) — H2, 4 critical factors.
3. Why {affiliate_name} is the Top Pick in 2026 (500 words) — H2. Sub-sections: Performance, Security, Pricing, Support. Second affiliate CTA here.
4. Pros & Cons of {affiliate_name} — H2, Markdown lists.
5. Alternative Options — H2. 2 brief alternatives, explain why {affiliate_name} still wins.
6. FAQ — H2. Answer 3 common questions on the keyword.
7. Conclusion & Final Verdict — H2. Summarize + final strong affiliate CTA.

AFFILIATE LINK: Embed exactly 3 times: [{affiliate_name}]({affiliate_url}) or [Get started with {affiliate_name}]({affiliate_url})

END THE ARTICLE WITH:
---
*Disclaimer: This article contains affiliate links. If you purchase through our links, we may earn a small commission at no extra cost to you.*

OUTPUT RULES:
- Output ONLY raw Markdown. No preambles, no meta-commentary.
- Tone: Professional, trustworthy, direct.
"""

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=120,
            )
            data = resp.json()

            if resp.status_code == 200:
                content = data["content"][0]["text"]
                print(f"    [+] Claude viết xong! ({len(content)} ký tự)")
                return content
            elif resp.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"    [!] Rate limit — chờ {wait}s...")
                time.sleep(wait)
            else:
                print(f"    [-] Lỗi API: {data.get('error', {}).get('message', resp.status_code)}")
                return None
        except Exception as e:
            print(f"    [-] Lỗi kết nối: {e}")
            time.sleep(10)
    return None

# ==========================================
# 5. LƯU FILE MARKDOWN (có frontmatter đầy đủ)
# ==========================================
def save_to_markdown(title, slug, content, keyword, img_path):
    now_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{now_date}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # Nếu file đã tồn tại, bỏ qua
    if os.path.exists(filepath):
        print(f"    [!] Bài đã tồn tại, bỏ qua: {filename}")
        return None

    clean = content.replace("#","").replace("*","").replace("\n"," ")
    description = clean[:155].strip()

    frontmatter = f"""---
title: "{title}"
date: {now_date}
slug: "{slug}"
draft: false
description: "{description}..."
keywords: ["{keyword}"]
categories: ["Hosting", "VPS"]
tags: ["vps", "hosting", "affiliate"]
cover:
  image: "{img_path}"
  alt: "{title}"
  relative: false
---

"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    print(f"    [+] Đã lưu: {filename}")
    return filepath

# ==========================================
# 6. PUSH LÊN GITHUB
# ==========================================
def push_to_github(success_count):
    try:
        os.chdir(REPO_PATH)
        print("\n[*] Đang đẩy lên GitHub...")

        lock = os.path.join(REPO_PATH, ".git", "index.lock")
        if os.path.exists(lock):
            os.remove(lock)

        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        msg = f"Auto: {success_count} bài mới [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
        result = subprocess.run(["git", "commit", "-m", msg], capture_output=True)

        if result.returncode != 0:
            stderr = result.stderr.decode() if result.stderr else ""
            if "nothing to commit" in stderr:
                print("[!] Không có gì mới để push.")
                return

        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print("[+] Push thành công! Web sẽ cập nhật sau 2 phút.")
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if e.stderr else ""
        print(f"[-] Lỗi Git: {stderr[:300]}")

# ==========================================
# 7. KHỞI CHẠY
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("   AI PRO FREELANCER — TỰ ĐỘNG VIẾT BÀI BẰNG CLAUDE")
    print("=" * 60)

    if not CLAUDE_API_KEY:
        print("\n⚠️  LỖI: Chưa có Claude API key!")
        print("     Tạo file claude_key.txt trong thư mục dự án")
        print("     rồi dán API key vào đó (không commit file này).")
        exit(1)

    success_count = 0
    total = len(ARTICLES)

    for i, art in enumerate(ARTICLES, 1):
        print(f"\n[{i}/{total}] {art['title']}")
        print("-" * 50)

        # Tạo ảnh bìa
        img_path = generate_cover_image(art["slug"], art["title"])

        # Sinh nội dung
        content = generate_content_with_claude(
            keyword=art["keyword"],
            title=art["title"],
            affiliate_url=art["affiliate_url"],
            affiliate_name=art["affiliate_name"],
        )

        if content:
            saved = save_to_markdown(
                title=art["title"],
                slug=art["slug"],
                content=content,
                keyword=art["keyword"],
                img_path=img_path,
            )
            if saved:
                success_count += 1

        if i < total:
            print(f"    [*] Nghỉ 5 giây...")
            time.sleep(5)

    if success_count > 0:
        push_to_github(success_count)

    print("\n" + "=" * 60)
    print(f"   XONG: {success_count}/{total} bài viết đã được publish!")
    print("=" * 60)
