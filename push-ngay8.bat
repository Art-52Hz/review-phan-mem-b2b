@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Add bai Writesonic vs Copy.ai...
git add content\posts\2026-06-19-writesonic-vs-copyai-2026.md

echo [2/3] Add cover image...
git add static\images\writesonic-vs-copyai-2026.webp

echo [3/3] Commit + Push...
git commit -m "Ngay 8: Writesonic vs Copy.ai 2026 comparison article + cover image"
git push origin main

echo.
echo === XONG! ===
echo Bai so sanh: https://aiprofreelancer.com/posts/writesonic-vs-copyai-2026/
echo.
echo Nho chay push-ngay7.bat neu chua push WebP + Grammarly!
pause
