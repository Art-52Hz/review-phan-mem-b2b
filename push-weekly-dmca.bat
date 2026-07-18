@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Add bai DMCA Ignored Hosting 2026...
git add content\posts\2026-06-29-dmca-ignored-hosting-2026.md

echo [2/3] Add cover image...
git add static\images\dmca-ignored-hosting-2026.webp

echo [3/3] Commit + Push...
git commit -m "Weekly: DMCA Ignored Hosting 2026 (1300+ words, offshore cluster)"
git push origin main

echo.
echo === XONG! ===
echo Bai moi: https://aiprofreelancer.com/posts/dmca-ignored-hosting-2026/
echo Cho GitHub Actions ~2 phut roi chay submit-indexnow.ps1
pause
