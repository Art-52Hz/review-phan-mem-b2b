@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-06-24-canva-review-2026.md
git add content\posts\2026-06-25-otter-ai-review-2026.md
git add content\posts\2026-06-26-activecampaign-review-2026.md
git add content\posts\2026-06-27-getresponse-vs-mailchimp-2026.md
git add static\images\canva-review-2026.webp
git add static\images\otter-ai-review-2026.webp
git add static\images\activecampaign-review-2026.webp
git add static\images\getresponse-vs-mailchimp-2026.webp
git commit -m "Days 12-15: Canva, Otter.ai, ActiveCampaign, GetResponse vs Mailchimp"
git push origin main
echo === XONG! ===
pause
