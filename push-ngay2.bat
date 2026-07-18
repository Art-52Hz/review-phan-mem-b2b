@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-06-12-writesonic-review-2026.md
git commit -m "Ngay 2: Rewrite Writesonic review - AI Search Engine (not writing tool)"
git push origin main
echo.
echo XONG! Build se chay trong 1-2 phut.
pause
