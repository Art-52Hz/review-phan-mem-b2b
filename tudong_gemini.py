import os
import subprocess
from datetime import datetime
import time
import requests
from urllib.parse import quote

# ==========================================
# 1. CẤU HÌNH HỆ THỐNG
# ==========================================
REPO_PATH = r"D:\projects\review-phan-mem-b2b"
POSTS_DIR = os.path.join(REPO_PATH, "content", "posts")

# Khai báo trực tiếp API Key của bạn vào đây
GEMINI_API_KEY = "AIzaSyCkRgjtbtR-esEa8Un4crJ86ZRoNH9BZUc" 


# ==========================================
# 2. DANH SÁCH BÀI VIẾT TỰ ĐỘNG
# ==========================================
ARTICLES = [
    {
        "keyword": "best offshore VPS hosting anonymous crypto payment 2026",
        "title": "Best Offshore VPS Hosting in 2026: Anonymous & Crypto-Friendly",
        "slug": "best-offshore-vps-hosting-anonymous-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "best VPS for freelancers cheap reliable 2026",
        "title": "Best VPS Hosting for Freelancers in 2026: Fast, Cheap & Reliable",
        "slug": "best-vps-for-freelancers-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
    {
        "keyword": "cheapest VPS accept bitcoin USDT crypto payment 2026",
        "title": "5 Cheapest VPS Providers That Accept Crypto Payment in 2026",
        "slug": "cheapest-vps-crypto-payment-2026",
        "affiliate_url": "https://ultahost.com/#art52hz",
        "affiliate_name": "UltaHost",
    },
]

# ==========================================
# 3. KỸ NĂNG CỦA CHUYÊN GIA SEO & TẠO ẢNH
# ==========================================
def generate_content_with_gemini(keyword, title, affiliate_url, affiliate_name):
    # Tạo URL ảnh tự động dựa trên từ khóa
    encoded_keyword = quote(f"high tech server data center {keyword}")
    cover_image_url = f"https://image.pollinations.ai/prompt/{encoded_keyword}?width=1200&height=630&nologo=true"
    
    encoded_mid_keyword = quote(f"cyber security anonymous cryptocurrency {keyword}")
    mid_image_url = f"https://image.pollinations.ai/prompt/{encoded_mid_keyword}?width=800&height=400&nologo=true"

    prompt = f"""Act as a Senior Technical SEO Expert and Expert Copywriter with 10+ years of experience reviewing VPS hosting. Write an extremely comprehensive, SEO-optimized blog post in English. Current year is 2026.

Keyword to rank for: '{keyword}'
Post Title: {title}

**SEO & FORMATTING RULES (CRITICAL FOR 90+ SCORE):**
1. **Keyword Placement:** Include '{keyword}' naturally in the FIRST 100 words, in at least one H2, one H3, and the conclusion.
2. **Readability:** MAXIMUM 3 sentences per paragraph. Use bolding for important metrics. Use bullet points frequently.
3. **Images (CRITICAL):** You must insert these exact image markdown tags at the specified locations to make the post visually appealing:
   - Right after the Introduction (H1/Title context), insert this cover image:
     ![{title}]({cover_image_url})
   - Under the "Security & Anonymity" or equivalent H2/H3 section, insert this illustration:
     ![Secure Crypto VPS]({mid_image_url})

**STRUCTURE OF THE POST:**
1. **Introduction (150 words):** Hook the reader. State what this covers. Add the first Affiliate CTA naturally here.
2. **Key Factors to Consider (200 words):** H2 heading. 4 critical factors when choosing this service.
3. **Why {affiliate_name} is the Top Pick in 2026 (500 words):** H2 heading. Comprehensive review of {affiliate_name}. 
   - Sub-headings (H3): Performance, Security & Anonymity, Pricing & Crypto Payments, Customer Support.
   - Add the second Affiliate CTA here naturally.
4. **Pros & Cons of {affiliate_name}:** H2 heading. Use Markdown lists.
5. **Alternative Options:** H2 heading. Briefly mention 2 other generic options and why {affiliate_name} still wins.
6. **Frequently Asked Questions (FAQ):** H2 heading. Answer 3 common questions related to the keyword.
7. **Conclusion & Final Verdict:** H2 heading. Summarize the value. Add the final strong Affiliate CTA.

**AFFILIATE LINK INSTRUCTIONS:**
- Embed the link exactly 3 times using this format: [{affiliate_name}]({affiliate_url}) or [Start your {affiliate_name} server today]({affiliate_url}).

**END THE ARTICLE EXACTLY WITH THIS:**
---
*Disclaimer: This article contains affiliate links. If you purchase a plan through our links, we may earn a small commission at no extra cost to you.*

**OUTPUT RULES:**
- Output ONLY raw Markdown text. No preambles.
- Tone: Professional, trustworthy, direct.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4000
        }
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            try:
                response_data = response.json()
            except Exception:
                print(f"    [-] Máy chủ Google bị lỗi mạng (Không trả về JSON). Status Code: {response.status_code}")
                time.sleep(10)
                continue

            if response.status_code == 200:
                content = response_data['candidates'][0]['content']['parts'][0]['text']
                print(f"    [+] Gemini viết xong! ({len(content)} ký tự, có kèm ảnh AI)")
                return content
            elif response.status_code == 429:
                wait_time = 45 * (attempt + 1)
                print(f"    [!] Quá tải Limit! Đang chờ {wait_time}s rồi thử lại lần {attempt + 1}...")
                time.sleep(wait_time)
            else:
                print(f"    [-] Lỗi từ Google API: {response_data.get('error', {}).get('message', 'Không xác định')}")
                return None

        except Exception as e:
            print(f"    [-] Lỗi kết nối: {e}")
            return None
    return None

# ==========================================
# 4. LƯU FILE MARKDOWN
# ==========================================
def save_to_markdown(title, slug, content, keyword):
    now_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{now_date}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    clean_content = content.replace("#", "").replace("*", "").replace("\n", " ")
    description = clean_content[:155].strip()

    markdown_template = f"""---
title: "{title}"
date: {now_date}
slug: "{slug}"
draft: false
description: "{description}..."
keywords: ["{keyword}", "vps offshore", "crypto vps", "ultahost review"]
categories: ["VPS Hosting"]
tags: ["vps", "offshore", "crypto", "affiliate", "hosting"]
---

{content}
"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_template)

    print(f"    [+] Đã lưu file: {filename}")
    return filepath

# ==========================================
# 5. ĐẨY LÊN GITHUB
# ==========================================
def push_to_github(success_count):
    try:
        os.chdir(REPO_PATH)
        print("\n[*] Đang đồng bộ lên GitHub Pages...")

        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        commit_msg = f"Auto-publish {success_count} posts (SEO 90+ & AI Images) [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
        
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)

        print("[+] Thành công! Chờ 2 phút để GitHub xuất bản Web.")
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if e.stderr else ""
        if "nothing to commit" in stderr:
            print("[!] Không có bài viết nào mới để đẩy lên.")
        else:
            print(f"[-] Lỗi Git: {stderr[:200]}")

# ==========================================
# 6. KHỞI CHẠY
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("   HỆ THỐNG VIẾT BÀI CHUẨN SEO 90+ KÈM ẢNH TỰ ĐỘNG")
    print("=" * 60)

    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_DIEN_VAO_DAY":
        print("\n⚠️ LỖI: Bạn chưa điền GEMINI_API_KEY ở dòng 15!")
        exit(1)

    success_count = 0
    total = len(ARTICLES)

    for i, article in enumerate(ARTICLES, 1):
        print(f"\n[{i}/{total}] Đang xử lý: {article['title']}")
        print("-" * 50)

        content = generate_content_with_gemini(
            keyword=article["keyword"],
            title=article["title"],
            affiliate_url=article["affiliate_url"],
            affiliate_name=article["affiliate_name"],
        )

        if content:
            save_to_markdown(
                title=article["title"],
                slug=article["slug"],
                content=content,
                keyword=article["keyword"],
            )
            success_count += 1
        
        if i < total:
            print(f"    [*] Đang nghỉ 30 giây để nhường đường cho AI...")
            time.sleep(30)

    if success_count > 0:
        push_to_github(success_count)

    print("\n" + "=" * 60)
    print(f"   HOÀN TẤT: {success_count}/{total} bài viết đã lên sóng!")
    print("=" * 60)