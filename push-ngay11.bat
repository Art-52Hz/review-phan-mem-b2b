@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Add Descript Review article...
git add content\posts\2026-06-23-descript-review-2026.md

echo [2/3] Add Descript cover image...
git add static\images\descript-review-2026.webp

echo [3/3] Commit + Push...
git commit -m "Ngay 11: Descript Review 2026 — AI video editor review + cover image"
git push origin main

echo.
echo === XONG! ===
echo Kiem tra: https://aiprofreelancer.com/posts/descript-review-2026/
pause
