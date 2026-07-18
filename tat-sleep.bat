@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo === TAT CHE DO NGU MAY TINH ===
echo.

:: Tat sleep khi dang cam sac (AC)
powercfg /change standby-timeout-ac 0
echo [+] Sleep khi cam sac: DA TAT

:: Tat sleep khi dung pin (DC)
powercfg /change standby-timeout-dc 0
echo [+] Sleep khi dung pin: DA TAT

:: Tat man hinh tat khi cam sac (tuy chon - bo comment neu muon giu)
:: powercfg /change monitor-timeout-ac 0

:: Tat hibernate
powercfg /hibernate off
echo [+] Hibernate: DA TAT

echo.
echo === HOAN TAT ===
echo May tinh se khong tu ngu trong khi automation chay.
echo.
pause
