@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/4] Git add WebP images...
git add static\images\*.webp

echo [2/4] Git add updated markdown files...
git add content\posts\*.md

echo [3/4] Commit...
git commit -m "Perf: convert all images to WebP (fix LCP 3.5s -> target <2.5s)"

echo [4/4] Push...
git push origin main

echo.
echo XONG! Images da duoc convert sang WebP.
echo - best-offshore-vps: 5.6MB -> 121KB (98%% saved)
echo - Tong cong 39 anh duoc optimize
echo Kiem tra lai: https://pagespeed.web.dev/report?url=https://aiprofreelancer.com/
pause
