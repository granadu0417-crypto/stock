@echo off
chcp 65001 > nul
echo ============================================
echo 키움증권 자동매매 프로그램 - 패키지 설치
echo ============================================
echo.

echo Python 버전 확인 중...
python --version
if errorlevel 1 (
    echo.
    echo [오류] Python이 설치되어 있지 않습니다!
    echo Python 3.8 이상을 설치해주세요.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 패키지 설치를 시작합니다...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [오류] 패키지 설치에 실패했습니다.
    echo 관리자 권한으로 다시 실행해보세요.
    pause
    exit /b 1
)

echo.
echo ============================================
echo 설치가 완료되었습니다!
echo 이제 "2_설정.bat"을 실행하세요.
echo ============================================
pause
