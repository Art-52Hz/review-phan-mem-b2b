@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-06-16-nordvpn-vs-expressvpn-2026.md
git add content\posts\2026-06-16-best-vpn-for-freelancers-2026.md
git commit -m "Ngay 4: NordVPN vs ExpressVPN + Best VPN for Freelancers (40%% commission)"
git push origin main
echo.
echo XONG! 2 bai moi se live trong 1-2 phut.
echo Kiem tra: https://aiprofreelancer.com
pause
