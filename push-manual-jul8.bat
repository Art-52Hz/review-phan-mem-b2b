@echo off
:: Manual push - July 8, 2026 (auto-push 21:00 didn't run)
cd /d "D:\projects\review-phan-mem-b2b"

if exist .git\index.lock del /f /q .git\index.lock

:: Modified tracked files (internal linking overhaul, 48 posts + configs)
git add -u

:: 3 new comparison posts + cover images
git add "content/posts/2026-06-29-ahrefs-vs-semrush-2026.md"
git add "content/posts/2026-06-29-nordvpn-vs-protonvpn-2026.md"
git add "content/posts/2026-06-29-systeme-io-vs-clickfunnels-2026.md"
git add "static/images/ahrefs-vs-semrush-2026.webp"
git add "static/images/nordvpn-vs-protonvpn-2026.webp"
git add "static/images/systeme-io-vs-clickfunnels-2026.webp"
git add "static/images/writesonic-vs-copyai-2026.png"

git commit -m "Content: 3 comparison posts + internal linking overhaul (Related Reviews on 48 posts)"
git push origin main

echo.
echo ============================================
echo   XONG! GitHub Actions se build va deploy.
echo   Kiem tra: https://github.com/Art-52Hz/review-phan-mem-b2b/actions
echo ============================================
pause
