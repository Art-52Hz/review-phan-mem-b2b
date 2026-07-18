@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add static\c1483141308e40cfaaee0f889553afa4.txt
git commit -m "Add IndexNow key for search engine indexing"
git push origin main
echo.
echo === KEY DA PUSH LEN GITHUB! ===
echo.
echo Sau khi push xong tat ca bai viet, chay:
echo   powershell -ExecutionPolicy Bypass -File submit-indexnow.ps1
echo.
echo === Google Search Console (lam thu cong) ===
echo 1. Vao: https://search.google.com/search-console
echo 2. Add property: aiprofreelancer.com (chon Domain)
echo 3. Xac minh bang DNS TXT record
echo 4. Submit sitemap: https://aiprofreelancer.com/sitemap.xml
echo.
pause
