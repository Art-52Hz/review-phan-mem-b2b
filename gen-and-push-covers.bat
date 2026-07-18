@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"

echo [1/3] Tao anh bia...
python gen-covers.py
if %errorLevel% neq 0 (
    echo [-] Loi khi tao anh! Kiem tra Python + Pillow.
    pause
    exit /b 1
)

echo.
echo [2/3] Git add + commit...
if exist .git\index.lock del /f /q .git\index.lock
git add static\images\nordvpn-review-2026.png
git add static\images\nordvpn-vs-expressvpn-2026.png
git add static\images\best-vpn-for-freelancers-2026.png
git add static\images\systeme-io-review-2026.png
git add static\images\writesonic-review-2026.png
git commit -m "Add cover images: NordVPN, Systeme.io, Writesonic, Best VPN"

echo.
echo [3/3] Push len GitHub...
git push origin main

echo.
echo XONG! Anh se hien thi sau 1-2 phut.
pause
