@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add .github\workflows\hugo.yml
git commit -m "Fix: add --buildFuture so all 30 articles are published (not just past-dated)"
git push origin main
echo.
echo === XONG! ===
echo Tat ca 30 bai se duoc xuat ban sau khi GitHub Actions chay xong (~2 phut)
echo Kiem tra tai: https://aiprofreelancer.com/posts/canva-review-2026/
echo.
pause
