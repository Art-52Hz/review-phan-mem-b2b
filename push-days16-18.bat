@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-06-28-monday-com-review-2026.md
git add content\posts\2026-06-29-loom-review-2026.md
git add content\posts\2026-06-30-beautiful-ai-review-2026.md
git add static\images\monday-com-review-2026.webp
git add static\images\loom-review-2026.webp
git add static\images\beautiful-ai-review-2026.webp
git commit -m "Days 16-18: Monday.com, Loom, Beautiful.ai reviews + cover images"
git push origin main
echo === XONG DAYS 16-18! ===
pause
