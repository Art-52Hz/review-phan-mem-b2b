@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "D:\projects\review-phan-mem-b2b"

if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Staging cover images + new posts...
git add static\images\nordvpn-review-2026.png
git add static\images\nordvpn-vs-expressvpn-2026.png
git add static\images\best-vpn-for-freelancers-2026.png
git add static\images\systeme-io-review-2026.png
git add content\posts\2026-06-16-nordvpn-review-2026.md
git add content\posts\2026-06-16-nordvpn-vs-expressvpn-2026.md
git add content\posts\2026-06-16-best-vpn-for-freelancers-2026.md
git add content\posts\2026-06-15-systeme-io-review-2026.md
git add content\posts\2026-06-12-writesonic-review-2026.md

echo [2/3] Committing...
git commit -m "Add cover images + new articles: NordVPN, Systeme.io, Writesonic"

echo [3/3] Pushing...
git push origin main

echo.
echo XONG! Anh bi va bai viet hien sau 1-2 phut.
echo Kiem tra: https://aiprofreelancer.com
pause
