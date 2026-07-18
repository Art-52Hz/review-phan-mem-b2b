@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Add bai Murf AI Review...
git add content\posts\2026-06-21-murf-ai-review-2026.md

echo [2/3] Add cover image...
git add static\images\murf-ai-review-2026.webp

echo [3/3] Commit + Push...
git commit -m "Ngay 10: Murf AI Review 2026 (1500+ words) + cover image"
git push origin main

echo.
echo === XONG! ===
echo Bai Murf AI: https://aiprofreelancer.com/posts/murf-ai-review-2026/
pause
