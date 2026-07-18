@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Add bai Notion AI Review...
git add content\posts\2026-06-20-notion-ai-review-2026.md

echo [2/3] Add cover image...
git add static\images\notion-ai-review-2026.webp

echo [3/3] Commit + Push...
git commit -m "Ngay 9: Notion AI Review 2026 (2000+ words)"
git push origin main

echo.
echo === XONG! ===
echo Bai Notion AI: https://aiprofreelancer.com/posts/notion-ai-review-2026/
echo.
echo NOTE: Notion Affiliate hien dong dang ky (thang 6/2026)
echo Theo doi tai: https://www.notion.com/affiliates
pause
