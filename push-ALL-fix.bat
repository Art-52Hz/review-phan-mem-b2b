@echo off
:: ============================================================
:: push-ALL-fix.bat — DEPLOY TẤT CẢ công việc đang bị kẹt
:: (best-free-tools, internal linking, freshness, indexnow...)
:: ============================================================
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [*] Add TAT CA thay doi (bao gom bai moi + internal linking + freshness)...
git add -A

echo [*] Commit...
git commit -m "Deploy backlog: best-free-tools lead magnet + internal linking + freshness (lastmod) + indexnow"

echo [*] Push len GitHub...
git push origin main

echo.
echo ============================================================
echo   XONG! Cho GitHub Actions build ~2-3 phut.
echo   Kiem tra: https://github.com/Art-52Hz/review-phan-mem-b2b/actions
echo   Sau do bai best-free-tools + Related Reviews se LEN LIVE.
echo ============================================================
pause
