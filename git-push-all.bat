@echo off
:: Tu dong yeu cau quyen Admin neu chua co
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Dang yeu cau quyen Administrator...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f .git\index.lock
if exist .git\refs\heads\main.lock del /f .git\refs\heads\main.lock

git add -A
git status
echo.
git commit -m "Add 7 new posts + .gitignore + security fix"
echo.
git push
echo.
echo =============================
echo   HOAN THANH! Kiem tra site:
echo   https://aiprofreelancer.com
echo =============================
pause
