"""Tao anh thumb rieng cho tung bai (24/11/2026).

    python tools/thumbs/gen_thumbs.py            # tao anh con thieu
    python tools/thumbs/gen_thumbs.py --all      # tao lai tat ca
    python tools/thumbs/gen_thumbs.py --only slug1,slug2

Ra: static/images/thumbs/<slug>.webp (1200x630). card_thumb.html tu dung anh nay neu co.
Logo: simple-icons (CC0) trong tools/thumbs/logos; hang khong co logo -> o chu ten hang.
Render bang Chrome that (playwright channel="chrome"), nen can Google Chrome tren may.
"""
import base64
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "content" / "posts"
OUT = ROOT / "static" / "images" / "thumbs"
HERE = Path(__file__).resolve().parent
COLORS = json.loads((HERE / "colors.json").read_text(encoding="utf-8"))

# (regex, key, ten hien thi, mau neu khong co trong simple-icons)
BRANDS = [
    (r"hostinger", "hostinger", "Hostinger", None),
    (r"ultahost", "ultahost", "UltaHost", "1F6FEB"),
    (r"contabo", "contabo", "Contabo", None),
    (r"elevenlabs", "elevenlabs", "ElevenLabs", None),
    (r"murf", "murf", "Murf AI", "6B4EFF"),
    (r"tradingview", "tradingview", "TradingView", None),
    (r"mangools|kwfinder", "mangools", "Mangools", "E8541E"),
    (r"semrush", "semrush", "Semrush", None),
    (r"ahrefs", "ahrefs", "Ahrefs", "FF8800"),
    (r"se ?ranking", "seranking", "SE Ranking", "2E8B57"),
    (r"surfer", "surfer", "Surfer", "1D4ED8"),
    (r"systeme", "systeme", "Systeme.io", "0FA3B1"),
    (r"clickfunnels", "clickfunnels", "ClickFunnels", "1C64F2"),
    (r"kajabi", "kajabi", "Kajabi", "2E3BFF"),
    (r"nordvpn", "nordvpn", "NordVPN", None),
    (r"expressvpn", "expressvpn", "ExpressVPN", None),
    (r"surfshark", "surfshark", "Surfshark", None),
    (r"protonvpn", "protonvpn", "Proton VPN", None),
    (r"jasper", "jasper", "Jasper", "7C3AED"),
    (r"writesonic", "writesonic", "Writesonic", "4F46E5"),
    (r"copy[ .-]?ai|copyai", "copyai", "Copy.ai", "111827"),
    (r"grammarly", "grammarly", "Grammarly", None),
    (r"notion", "notion", "Notion", None),
    (r"obsidian", "obsidian", "Obsidian", None),
    (r"canva", "canva", "Canva", None),
    (r"figma", "figma", "Figma", None),
    (r"descript", "descript", "Descript", "0B0B0B"),
    (r"otter", "otter", "Otter.ai", "1E6BFF"),
    (r"loom", "loom", "Loom", None),
    (r"beautiful[ .-]?ai|beautifulai", "beautifulai", "Beautiful.ai", "2563EB"),
    (r"midjourney", "midjourney", "Midjourney", "111111"),
    (r"zapier", "zapier", "Zapier", None),
    (r"hubspot", "hubspot", "HubSpot", None),
    (r"clickup", "clickup", "ClickUp", None),
    (r"monday", "monday", "monday.com", "FF3D57"),
    (r"webflow", "webflow", "Webflow", None),
    (r"typeform", "typeform", "Typeform", None),
    (r"activecampaign", "activecampaign", "ActiveCampaign", "356AE6"),
    (r"getresponse", "getresponse", "GetResponse", "00A2FF"),
    (r"mailchimp", "mailchimp", "Mailchimp", None),
    (r"\bkit\b|convertkit", "kit", "Kit", None),
    (r"n8n", "n8n", "n8n", None),
    (r"docker", "docker", "Docker", None),
    (r"ollama", "ollama", "Ollama", None),
    (r"plex", "plex", "Plex", None),
    (r"nextcloud", "nextcloud", "Nextcloud", None),
    (r"odoo", "odoo", "Odoo", None),
    (r"node\.?js", "nodedotjs", "Node.js", None),
    (r"wireguard", "wireguard", "WireGuard", None),
    (r"discord", "discord", "Discord", None),
    (r"wordpress", "wordpress", "WordPress", None),
    (r"minecraft", "minecraft", "Minecraft", "3C8527"),
    (r"\bmt4\b|\bmt5\b|metatrader", "metatrader", "MT4 / MT5", "0E5FA8"),
]

TOPICS = {  # nen: (dam, nhat)
    "vps": ("#0b3b38", "#0f766e"), "voice": ("#2e1065", "#7c3aed"), "trade": ("#052e16", "#15803d"),
    "seo": ("#431407", "#c2410c"), "vpn": ("#0c1e4a", "#1d4ed8"), "mkt": ("#500724", "#be185d"),
    "ai": ("#1e1b4b", "#4338ca"),
}
ICONS = {
    "vps": '<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01M11 7h6M11 17h6"/>',
    "voice": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M8 21h8"/>',
    "trade": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 6-7"/><path d="M16 7h4v4"/>',
    "seo": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>',
    "vpn": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "mkt": '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
    "ai": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/>',
}


def front(md):
    m = re.match(r"---\n(.*?)\n---", md, re.S)
    fm = m.group(1) if m else ""
    def get(k):
        r = re.search(rf'^{k}:\s*"?(.*?)"?\s*$', fm, re.M)
        return r.group(1) if r else ""
    tags = " ".join(re.findall(r'"([^"]+)"', " ".join(re.findall(r"^(?:tags|categories):.*$", fm, re.M))))
    return get("title"), get("slug"), get("draft"), tags


def topic_of(t):
    t = t.lower()
    if re.search(r"tradingview|forex|mt4|mt5|trading", t): return "trade"
    if re.search(r"vpn|security|privacy", t): return "vpn"
    if re.search(r"vps|hosting|server|wordpress|n8n|docker|minecraft|dmca|rdp", t): return "vps"
    if re.search(r"voice|elevenlabs|murf|audio|narration|voiceover", t): return "voice"
    if re.search(r"seo|keyword|kwfinder|mangools|semrush|ahrefs|surfer", t): return "seo"
    if re.search(r"systeme|funnel|email|newsletter|marketing|kajabi|course", t): return "mkt"
    return "ai"


def kind_of(title):
    head = title.split(":", 1)[0]
    for t in (head, title):
        if re.search(r"(?i)\bvs\.?\b|compared", t): return "Comparison"
        if re.search(r"(?i)alternatives", t): return "Alternatives"
        if re.search(r"(?i)black friday", t): return "Black Friday"
        if re.search(r"(?i)review", t): return "Review"
        if re.search(r"(?i)^(best|cheapest)", t): return "Best of"
        if re.search(r"(?i)pricing|price|cost|coupon|discount|renewal|plans", t): return "Pricing"
    return "Guide"


def brands_in(text):
    found = []
    low = text.lower()
    for rx, key, name, color in BRANDS:
        m = re.search(rx, low)
        if m and key not in [f[0] for f in found]:
            found.append((key, name, "#" + (COLORS.get(key) or color or "111827"), m.start()))
    found.sort(key=lambda f: f[3])
    return found[:2]


def logo_tile(key, name, color):
    svg = HERE / "logos" / f"{key}.svg"
    if svg.exists():
        raw = svg.read_text(encoding="utf-8").replace("<svg ", f'<svg fill="{color}" ', 1)
        inner = f'<img src="data:image/svg+xml;base64,{base64.b64encode(raw.encode()).decode()}" alt="">'
        return f'<div class="tile"><div class="logo">{inner}</div><div class="bn">{name}</div></div>'
    return f'<div class="tile"><div class="word" style="color:{color}">{name}</div></div>'


def split_title(title):
    t = re.sub(r"\s*\(?\b20\d\d\b\)?(?=\s*(:|$))", "", title).strip()
    if ":" in t:
        a, b = t.split(":", 1)
        return a.strip(), b.strip()
    return t, ""


def html(title, tags, slug):
    topic = topic_of(f"{title} {tags} {slug}")
    dark, light = TOPICS[topic]
    head, sub = split_title(title)
    kind = kind_of(title)
    br = brands_in(f"{title} {slug}")
    if len(br) == 2:
        right = logo_tile(*br[0][:3]) + '<div class="vs">VS</div>' + logo_tile(*br[1][:3])
    elif br:
        right = logo_tile(*br[0][:3])
    else:
        right = f'<div class="tile"><svg class="ticon" viewBox="0 0 24 24" fill="none" stroke="{light}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[topic]}</svg></div>'
    size = 64 if len(head) < 26 else 56 if len(head) < 40 else 48
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&display=swap');
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;font-family:Inter,Segoe UI,sans-serif;color:#fff;overflow:hidden;
 background:radial-gradient(circle at 85% 20%,{light} 0,transparent 55%),linear-gradient(135deg,{dark} 0%,{light} 140%);position:relative}}
body:before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:40px 40px;
 -webkit-mask-image:linear-gradient(90deg,transparent 30%,#000 100%)}}
.wrap{{position:absolute;inset:0;display:flex;align-items:center;padding:0 64px;gap:40px}}
.left{{flex:1;min-width:0}}
.kind{{display:inline-block;padding:8px 16px;border-radius:999px;background:rgba(255,255,255,.16);font-weight:700;font-size:20px;letter-spacing:.06em;text-transform:uppercase}}
h1{{font-size:{size}px;line-height:1.08;font-weight:800;letter-spacing:-.02em;margin:22px 0 0}}
p{{font-size:24px;line-height:1.35;font-weight:500;opacity:.85;margin-top:18px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.right{{display:flex;align-items:center;gap:18px;flex-shrink:0}}
.tile{{width:230px;height:230px;border-radius:36px;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;
 box-shadow:0 30px 60px rgba(0,0,0,.35)}}
.logo img{{width:110px;height:110px;display:block}}
.bn{{color:#111827;font-weight:800;font-size:24px}}
.word{{font-weight:800;font-size:34px;text-align:center;padding:0 14px;line-height:1.1}}
.ticon{{width:130px;height:130px}}
.vs{{width:64px;height:64px;border-radius:50%;background:#f59e0b;color:#1f1300;font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center;margin:0 -40px;z-index:2;box-shadow:0 8px 20px rgba(0,0,0,.3)}}
.brand{{position:absolute;left:64px;bottom:36px;font-weight:700;font-size:20px;opacity:.75}}
</style></head><body><div class="wrap"><div class="left"><span class="kind">{kind}</span><h1>{head}</h1>{f"<p>{sub}</p>" if sub else ""}</div>
<div class="right">{right}</div></div><div class="brand">aiprofreelancer.com</div></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = next((a.split(",") for a in [x.split("=", 1)[1] for x in sys.argv if x.startswith("--only=")]), None)
    jobs = []
    for f in sorted(POSTS.glob("*.md")):
        title, slug, draft, tags = front(f.read_text(encoding="utf-8"))
        slug = slug or f.stem
        if draft == "true" or not title:
            continue
        if only and slug not in only:
            continue
        if not only and "--all" not in sys.argv and (OUT / f"{slug}.webp").exists():
            continue
        jobs.append((slug, title, tags))
    if not jobs:
        print("Khong co anh can tao"); return
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for slug, title, tags in jobs:
            pg.set_content(html(title, tags, slug), wait_until="networkidle")
            png = OUT / f"{slug}.png"
            pg.screenshot(path=str(png))
            from PIL import Image
            Image.open(png).convert("RGB").save(OUT / f"{slug}.webp", "WEBP", quality=82)
            png.unlink()
            print("OK", slug)
        b.close()


if __name__ == "__main__":
    main()
