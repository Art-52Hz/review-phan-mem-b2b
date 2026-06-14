@echo off
:: ============================================================
:: SETUP-SCHEDULER.BAT — Đăng ký chạy tự động hàng ngày
:: Chỉ cần chạy MỘT LẦN để cài đặt
:: ============================================================

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [*] Dang yeu cau quyen Admin...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ============================================================
echo   DANG KY TASK SCHEDULER - CHAY 1 LAN LA XONG
echo ============================================================
echo.

:: Xóa task cũ nếu có
schtasks /delete /tn "AIProFreelancer-AutoPublish" /f >nul 2>&1

:: Đăng ký task mới: chạy hàng ngày lúc 9:00 sáng
schtasks /create ^
    /tn "AIProFreelancer-AutoPublish" ^
    /tr "\"D:\projects\review-phan-mem-b2b\auto-publish.bat\" silent" ^
    /sc DAILY ^
    /st 21:00 ^
    /ru SYSTEM ^
    /rl HIGHEST ^
    /f

if %errorLevel% equ 0 (
    echo.
    echo [+] THANH CONG! Task da duoc dang ky:
    echo     Ten task : AIProFreelancer-AutoPublish
    echo     Lich trinh: Hang ngay luc 21:00 toi
    echo     Script   : auto-publish.bat
    echo.
    echo [*] De kiem tra, mo Task Scheduler va tim "AIProFreelancer-AutoPublish"
    echo [*] De chay ngay lap tuc, go lenh:
    echo     schtasks /run /tn "AIProFreelancer-AutoPublish"
    echo.
) else (
    echo [-] Loi khi dang ky task! Ma loi: %errorLevel%
    echo     Hay chay file nay voi quyen Administrator.
)

echo Nhan phim bat ky de dong...
pause >nul
