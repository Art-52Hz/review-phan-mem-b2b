@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/3] Staging...
git add content\posts\ hugo.toml .gitignore tudong_gemini.py

echo [2/3] Committing...
git commit -m "Fix YAML frontmatter (17 files) + author=Vincent Pham + Claude API"

echo [3/3] Pushing...
git push origin main

echo.
echo ============================================================
echo   XONG! GitHub Actions se build lai trong 1-2 phut.
echo   Anh bi la se hien sau khi build xong.
echo ============================================================
pause
