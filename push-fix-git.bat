@echo off
REM ============================================
REM  FIX GIT KẸT + PUSH TẤT CẢ (bài 13/7 + fixes)
REM  Nguyên nhân: git.exe treo từ 29/6 giữ .git\index
REM  → tudong_gemini.py fail 3 tuần, bài không lên live
REM ============================================
cd /d D:\projects\review-phan-mem-b2b

echo [1/5] Kill git process treo...
taskkill /F /IM git.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/5] Xoa file khoa cu...
if exist .git\index.lock del /F .git\index.lock

echo [3/5] Git add...
git add -A
if errorlevel 1 (
  echo !!! git add van loi - hay RESTART MAY roi chay lai file nay
  pause
  exit /b 1
)

echo [4/5] Commit...
git commit -m "Weekly 13-18/7: 2 money-pages (Crypto Trading Bot VPS + Anonymous VPS Providers) + inbound links + IndexNow 60 URLs + unstick git"

echo [5/5] Push len GitHub...
git push origin main
if errorlevel 1 (
  echo !!! Push loi - kiem tra mang / dang nhap GitHub
  pause
  exit /b 1
)

echo.
echo ===== XONG! Cho GitHub Actions ~2 phut roi kiem tra: =====
echo https://aiprofreelancer.com/posts/best-vps-for-crypto-trading-bots-2026/
pause
