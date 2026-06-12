@echo off
cd /d "%~dp0"
del .git\index.lock 2>nul
git add content/posts/2026-06-12-jasper-ai-review.md
git commit -m "Add Jasper AI review 2026"
git push
echo.
echo Done! Press any key to close.
pause
