@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-06-12-semrush-review-2026.md
git add static\images\semrush-review-2026.png
git commit -m "Ngay 5: Semrush review 2026 upgraded to 2200+ words"
git push origin main
echo.
echo XONG! Bai Semrush da duoc cap nhat.
echo Kiem tra: https://aiprofreelancer.com/semrush-review-2026/
pause
