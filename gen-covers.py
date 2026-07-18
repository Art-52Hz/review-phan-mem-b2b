"""
gen-covers.py — Tạo ảnh bìa cho các bài viết chưa có ảnh
Chạy: python gen-covers.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = r"D:\projects\review-phan-mem-b2b\static\images"

THEMES = {
    "vps":      ((15, 32, 80),   (30, 90, 200)),
    "hosting":  ((10, 40, 70),   (20, 100, 160)),
    "ai":       ((40, 15, 80),   (100, 40, 180)),
    "writing":  ((15, 60, 50),   (30, 140, 100)),
    "seo":      ((70, 40, 10),   (170, 100, 20)),
    "vpn":      ((10, 50, 40),   (20, 130, 100)),
    "security": ((50, 10, 30),   (130, 20, 60)),
    "systeme":  ((10, 60, 80),   (20, 140, 180)),
    "default":  ((20, 20, 50),   (50, 80, 150)),
}

def _get_theme(slug, title):
    t = (slug + title).lower()
    if "vpn" in t or "nordvpn" in t or "expressvpn" in t: return THEMES["vpn"]
    if "security" in t or "protect" in t or "nord" in t:  return THEMES["security"]
    if "systeme" in t:      return THEMES["systeme"]
    if "vps" in t:          return THEMES["vps"]
    if "hosting" in t:      return THEMES["hosting"]
    if "writing" in t or "copy" in t or "jasper" in t or "writesonic" in t: return THEMES["writing"]
    if "seo" in t or "surfer" in t: return THEMES["seo"]
    if "ai" in t:           return THEMES["ai"]
    return THEMES["default"]

def _wrap(text, max_chars=28):
    words = text.split()
    lines, line = [], ""
    for w in words:
        if len(line) + len(w) + 1 <= max_chars:
            line = (line + " " + w).strip()
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines[:4]  # max 4 dòng

def generate_cover(slug, title):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    out = os.path.join(IMAGES_DIR, f"{slug}.png")
    if os.path.exists(out):
        print(f"  [skip] {slug}.png (đã có)")
        return

    W, H = 1200, 630
    c1, c2 = _get_theme(slug, title)
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img, "RGBA")

    # Gradient nền
    for y in range(H):
        t = (y / H) ** 2
        r = int(c1[0]*(1-t) + c2[0]*t)
        g = int(c1[1]*(1-t) + c2[1]*t)
        b = int(c1[2]*(1-t) + c2[2]*t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Grid lines
    for x in range(0, W, 120): draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 12))
    for y in range(0, H, 120): draw.line([(0, y), (W, y)], fill=(255, 255, 255, 12))

    # Circles
    cx, cy = W - 100, -80
    for r in [280, 220, 160]:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(255, 255, 255, 18), width=2)

    # Bottom bar
    draw.rectangle([0, H-6, W, H], fill=(255, 255, 255, 60))

    # Fonts
    try:
        font_t = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 68)
        font_d = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26)
    except:
        font_t = ImageFont.load_default()
        font_d = font_t

    lines = _wrap(title)
    line_h = 82
    start_y = (H - len(lines) * line_h) // 2 - 30

    # Accent bar trên text
    draw.rectangle([60, start_y - 20, 160, start_y - 14], fill=(255, 255, 255, 150))

    for i, ln in enumerate(lines):
        y = start_y + i * line_h
        draw.text((62, y + 4), ln, font=font_t, fill=(0, 0, 0, 100))   # shadow
        draw.text((60, y),     ln, font=font_t, fill=(255, 255, 255, 255))

    draw.text((60, H - 52), "aiprofreelancer.com", font=font_d, fill=(255, 255, 255, 180))

    img.save(out, "PNG", optimize=True)
    print(f"  [+] Tạo xong: {slug}.png")

# ── Danh sách bài cần tạo ảnh ──────────────────────────────
ARTICLES = [
    ("nordvpn-review-2026",            "NordVPN Review 2026"),
    ("nordvpn-vs-expressvpn-2026",     "NordVPN vs ExpressVPN 2026"),
    ("best-vpn-for-freelancers-2026",  "Best VPN for Freelancers 2026"),
    ("systeme-io-review-2026",         "Systeme.io Review 2026"),
    ("writesonic-review-2026",         "Writesonic Review 2026"),
]

if __name__ == "__main__":
    print("=== Tạo ảnh bìa cho bài viết mới ===\n")
    for slug, title in ARTICLES:
        generate_cover(slug, title)
    print("\n=== XONG! Ảnh đã lưu vào static/images/ ===")
