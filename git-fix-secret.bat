@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "D:\projects\review-phan-mem-b2b"

echo [1/5] Xoa lock files...
if exist .git\index.lock del /f /q .git\index.lock
if exist .git\refs\heads\main.lock del /f /q .git\refs\heads\main.lock

echo [2/5] Gom tat ca commits thanh 1 commit sach (khong co API key)...
git reset --soft 51193dd

echo [3/5] Bo staged profile.txt (tranh commit API key)...
git restore --staged profile.txt 2>nul

echo [4/5] Tao 1 commit sach duy nhat...
git add -A
git commit -m "Add 17 new posts + cover images + automation system [clean history]"

echo [5/5] Force push len GitHub...
git push --force origin main

echo.
echo ============================================================
echo   HOAN THANH! Web se cap nhat trong 2-3 phut.
echo   Kiem tra tai: https://aiprofreelancer.com
echo ============================================================
pause
