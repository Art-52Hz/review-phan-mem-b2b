@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/5] Add WebP images (39 files)...
git add static\images\*.webp

echo [2/5] Add updated markdown files (front matter .webp)...
git add content\posts\*.md

echo [3/5] Add bai Grammarly...
git add content\posts\2026-06-18-grammarly-review-2026.md

echo [4/5] Add cover images Grammarly...
git add static\images\grammarly-review-2026.png
git add static\images\grammarly-review-2026.webp

echo [5/5] Commit + Push...
git commit -m "Ngay 7: Grammarly review 2026 + convert 39 images to WebP (fix LCP)"
git push origin main

echo.
echo === XONG! ===
echo Bai Grammarly: https://aiprofreelancer.com/posts/grammarly-review-2026/
echo PageSpeed kiem tra: https://pagespeed.web.dev/report?url=https://aiprofreelancer.com/
pause
