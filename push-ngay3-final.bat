@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-06-12-writesonic-review-2026.md
git add content\posts\2026-06-15-systeme-io-review-2026.md
git add content\posts\2026-06-16-nordvpn-review-2026.md
git add profile.txt
git commit -m "Ngay 3: Add NordVPN review (40%%) + Systeme.io (60%%) + fix Writesonic"
git push origin main
echo.
echo XONG! 3 bai moi se live trong 1-2 phut.
echo Kiem tra: https://aiprofreelancer.com
pause
