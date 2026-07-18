@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-07-01-kit-review-2026.md
git add content\posts\2026-07-02-figma-review-2026.md
git add content\posts\2026-07-03-zapier-review-2026.md
git add content\posts\2026-07-04-hubspot-review-2026.md
git add content\posts\2026-07-05-jasper-ai-review-2026.md
git add content\posts\2026-07-06-typeform-review-2026.md
git add content\posts\2026-07-07-ahrefs-review-2026.md
git add content\posts\2026-07-08-notion-vs-obsidian-2026.md
git add content\posts\2026-07-09-midjourney-review-2026.md
git add content\posts\2026-07-10-clickup-review-2026.md
git add content\posts\2026-07-11-webflow-review-2026.md
git add content\posts\2026-07-12-best-ai-tools-2026.md
git add static\images\kit-review-2026.webp
git add static\images\figma-review-2026.webp
git add static\images\zapier-review-2026.webp
git add static\images\hubspot-review-2026.webp
git add static\images\jasper-ai-review-2026.webp
git add static\images\typeform-review-2026.webp
git add static\images\ahrefs-review-2026.webp
git add static\images\notion-vs-obsidian-2026.webp
git add static\images\midjourney-review-2026.webp
git add static\images\clickup-review-2026.webp
git add static\images\webflow-review-2026.webp
git add static\images\best-ai-tools-2026.webp
git commit -m "Days 19-30: Kit, Figma, Zapier, HubSpot, Jasper, Typeform, Ahrefs, Notion vs Obsidian, Midjourney, ClickUp, Webflow, Best AI Tools Roundup"
git push origin main
echo === XONG DAYS 19-30! CHIEN DICH 30 NGAY HOAN THANH! ===
pause
