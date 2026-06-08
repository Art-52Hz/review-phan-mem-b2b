# HƯỚNG DẪN CÀI ĐẶT & SỬ DỤNG
# youtube_to_blog.py — aiprofreelancer.com

---

## BƯỚC 1 — Cài packages (chạy 1 lần)

```powershell
pip install anthropic youtube-transcript-api python-slugify
```

---

## BƯỚC 2 — Set API Key

```powershell
# Windows PowerShell — set 1 lần, dùng mãi
$env:ANTHROPIC_API_KEY = "sk-ant-api03-YOUR-KEY-HERE"

# Hoặc set permanent (không cần set lại mỗi lần mở PowerShell)
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-YOUR-KEY-HERE", "User")
```

> Lấy API key tại: https://console.anthropic.com/settings/keys

---

## BƯỚC 3 — Chạy script

### Ví dụ 1 — Review Notion AI
```powershell
python youtube_to_blog.py `
  --url "https://youtube.com/watch?v=VIDEO_ID" `
  --keyword "notion ai review 2026" `
  --product "Notion AI" `
  --affiliate "https://notion.so/your-affiliate"
```

### Ví dụ 2 — Review UltaHost (affiliate của bạn)
```powershell
python youtube_to_blog.py `
  --url "https://youtube.com/watch?v=VIDEO_ID" `
  --keyword "ultahost vps review 2026" `
  --product "UltaHost VPS" `
  --affiliate "https://ultahost.com/#art52hz"
```

### Ví dụ 3 — Review Jasper AI
```powershell
python youtube_to_blog.py `
  --url "https://youtube.com/watch?v=VIDEO_ID" `
  --keyword "jasper ai review 2026" `
  --product "Jasper AI" `
  --affiliate "https://jasper.ai/your-affiliate"
```

---

## BƯỚC 4 — Lấy file và upload Hugo

```powershell
# File được lưu tại:
# ./output_posts/[keyword-slug].md

# Copy vào Hugo project
Copy-Item "./output_posts/*.md" "D:\projects\review-phan-mem-b2b\content\posts\"

# Commit và push
cd D:\projects\review-phan-mem-b2b
git add content/posts/
git commit -m "Add new review post"
git push
```

---

## CHI PHÍ API ƯỚC TÍNH

| Bài viết | Tokens dùng | Chi phí |
|---|---|---|
| 1 bài | ~8,000 tokens | ~$0.08 |
| 10 bài | ~80,000 tokens | ~$0.80 |
| 50 bài | ~400,000 tokens | ~$4.00 |

**$5 API = ~60 bài viết hoàn chỉnh** ✅

---

## XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "TranscriptsDisabled"
```
Video đã tắt transcript → Tìm video khác có transcript
```

### Lỗi: "NoTranscriptFound"  
```
Không có transcript tiếng Anh → Tìm video khác
hoặc dùng video có CC (Closed Captions)
```

### Lỗi: "Authentication error"
```
API key sai hoặc chưa set
→ Kiểm tra: echo $env:ANTHROPIC_API_KEY
→ Set lại API key như Bước 2
```

### Lỗi: "credit_balance_too_low"
```
Hết credit → Nạp thêm tại console.anthropic.com
```

---

## TÌM VIDEO TỐT ĐỂ CHẠY

### Search trên YouTube:
```
notion ai review 2026 honest
jasper ai review 2026 freelancer
semrush review 2026 worth it
ahrefs vs semrush 2026
best ai writing tool 2026
```

### Tiêu chí video tốt:
- ✅ Views > 10,000
- ✅ Thời lượng 8-20 phút
- ✅ Channel liên quan tech/freelance
- ✅ Có CC hoặc auto-generated captions
- ❌ Tránh: Video do brand tự làm

---

## OUTPUT FILE MẪU

```
output_posts/
└── notion-ai-review-2026.md    ← Hugo-ready, schema included
```

File .md bao gồm:
- ✅ Front matter đầy đủ (date, author, schema, tags)
- ✅ Schema markup (Review type, rating, author)
- ✅ Cover image placeholder
- ✅ Full article 1,800+ từ
- ✅ 3 CTA với affiliate link
- ✅ Pros & Cons thật
- ✅ Comparison table
- ✅ FAQ section
- ✅ Affiliate disclosure
