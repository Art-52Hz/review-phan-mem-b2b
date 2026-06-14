@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "D:\projects\review-phan-mem-b2b"

if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Staging cover images + updated posts...
git add static\images\ content\posts\

echo [2/3] Committing...
git commit -m "Add local cover images for all 22 posts (replace Pollinations AI)"

echo [3/3] Pushing...
git push origin main

echo.
echo ============================================================
echo   XONG! Anh bi la da duoc fix.
echo   Web se cap nhat trong 2-3 phut.
echo ============================================================
pause
