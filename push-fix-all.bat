@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock

echo [1/5] Fix Grammarly + Writesonic cover image format...
git add content\posts\2026-06-18-grammarly-review-2026.md
git add content\posts\2026-06-19-writesonic-vs-copyai-2026.md

echo [2/5] Add all WebP cover images...
git add static\images\grammarly-review-2026.webp
git add static\images\writesonic-vs-copyai-2026.webp
git add static\images\notion-ai-review-2026.webp
git add static\images\murf-ai-review-2026.webp

echo [3/5] Add Notion AI Review (English)...
git add content\posts\2026-06-20-notion-ai-review-2026.md

echo [4/5] Add Murf AI Review (English)...
git add content\posts\2026-06-21-murf-ai-review-2026.md

echo [5/5] Commit + Push...
git commit -m "Fix: cover images + EN rewrites + ElevenLabs affiliate links in Murf review"
git push origin main

echo.
echo === XONG! ===
echo Kiem tra:
echo - https://aiprofreelancer.com/posts/grammarly-review-2026/
echo - https://aiprofreelancer.com/posts/writesonic-vs-copyai-2026/
echo - https://aiprofreelancer.com/posts/notion-ai-review-2026/
echo - https://aiprofreelancer.com/posts/murf-ai-review-2026/
pause
