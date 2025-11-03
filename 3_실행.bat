@echo off
chcp 65001 > nul
echo ============================================
echo 키움증권 자동매매 프로그램 (GUI)
echo ============================================
echo.
echo 프로그램을 시작합니다...
echo.

python main_gui.py

if errorlevel 1 (
    echo.
    echo [오류] 프로그램 실행에 실패했습니다.
    echo "2_설정.bat"으로 API 키를 먼저 설정하세요.
    pause
    exit /b 1
)
