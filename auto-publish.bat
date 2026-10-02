@echo off
:: ============================================================
:: AUTO-PUBLISH.BAT — Tự động viết bài + đẩy lên GitHub
:: Chạy hàng ngày qua Windows Task Scheduler
:: ============================================================

:: Read-only preflight by default. No elevation or automatic paid generation.

echo ============================================================
echo   AI PRO FREELANCER - HE THONG TU DONG XAY DUNG NOI DUNG
echo ============================================================
echo.

:: --- Xóa lock file nếu có ---
:: Preserve Git locks: an existing lock can belong to an active process.

:: --- Chạy script Python ---
echo [*] Bat dau tao bai viet tu dong...
cd /d "D:\projects\review-phan-mem-b2b"

python tudong_gemini.py

if %errorLevel% neq 0 (
    echo [-] Script Python gap loi! Ma loi: %errorLevel%
    echo.
    echo Kiem tra:
    echo   1. Python da duoc cai dat chua? (python --version)
    echo   2. Thu vien requests va Pillow da cai chua? (pip install requests pillow)
    echo   3. claude_key.txt co API key hop le khong?
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   HOAN TAT! Kiem tra web tai: https://aiprofreelancer.com
echo ============================================================

:: Nếu chạy thủ công (không phải Task Scheduler), pause để xem kết quả
if "%1" neq "silent" (
    echo.
    echo Nhan phim bat ky de dong...
    pause >nul
)
