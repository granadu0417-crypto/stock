@echo off
chcp 65001 > nul
echo ============================================
echo 키움증권 자동매매 프로그램 - API 설정
echo ============================================
echo.
echo API 키 설정 화면을 엽니다...
echo.

python config_gui.py

if errorlevel 1 (
    echo.
    echo [오류] 설정 프로그램 실행에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo 설정이 완료되었습니다.
pause
