@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "D:\projects\review-phan-mem-b2b"
if exist .git\index.lock del /f /q .git\index.lock
git add content\posts\2026-06-12-notion-ai-review-2026.md
git add content\posts\2026-06-12-murf-ai-review-2026.md
git add content\posts\2026-06-12-jasper-ai-review.md
git add submit-indexnow.ps1
git add content\posts\2026-06-16-best-vpn-for-freelancers-2026.md
git add content\posts\2026-06-17-nordvpn-vs-surfshark-2026.md
git add static\images\nordvpn-vs-surfshark-2026.webp
git add content\posts\best-offshore-vps-hosting-2026.md
git add content\posts\2026-06-25-otter-ai-review-2026.md
git add .gitignore
git commit -m "SEO: dedupe posts + fix IndexNow URLs + NordProtect CTA + new NordVPN vs Surfshark money-page"
git push origin main
echo.
echo === XONG! ===
echo GitHub Actions se rebuild ~2 phut. Sau do moi chay submit-indexnow.ps1
echo.
pause
