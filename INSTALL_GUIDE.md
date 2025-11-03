# 🚀 키움증권 자동매매 프로그램 - 설치 및 실행 가이드

## 📋 목차
1. [Python 설치 확인](#1-python-설치-확인)
2. [프로젝트 폴더 다운로드](#2-프로젝트-폴더-다운로드)
3. [패키지 설치](#3-패키지-설치)
4. [API 키 설정](#4-api-키-설정)
5. [프로그램 실행](#5-프로그램-실행)

---

## 1. Python 설치 확인

### Windows 사용자

1. **명령 프롬프트 열기**
   - `Windows 키` + `R` 누르기
   - `cmd` 입력 후 엔터

2. **Python 설치 확인**
   ```cmd
   python --version
   ```

   - Python 3.8 이상이 표시되면 OK!
   - 없으면 [Python 공식 사이트](https://www.python.org/downloads/)에서 다운로드

---

## 2. 프로젝트 폴더 다운로드

GitHub에서 프로젝트를 다운로드하거나 클론하세요.

```cmd
git clone [저장소 주소]
```

또는 ZIP 파일로 다운로드 후 압축 해제

---

## 3. 패키지 설치 ⭐ (중요!)

### Windows 사용자

#### 방법 1: 파일 탐색기에서 바로 실행 (제일 쉬움!)

1. **프로젝트 폴더 열기**
   - `stock` 폴더를 파일 탐색기로 열기
   - `requirements.txt` 파일이 보이는지 확인

2. **주소창에서 cmd 실행**
   - 파일 탐색기 상단의 **주소창**을 클릭
   - `cmd` 입력 후 엔터
   - 자동으로 해당 폴더에서 명령 프롬프트가 열립니다!

3. **패키지 설치 명령어 입력**
   ```cmd
   pip install -r requirements.txt
   ```

#### 방법 2: 수동으로 경로 이동

1. **명령 프롬프트 열기**
   - `Windows 키` + `R`
   - `cmd` 입력 후 엔터

2. **프로젝트 폴더로 이동**
   ```cmd
   cd C:\Users\사용자이름\다운로드\stock
   ```
   (실제 프로젝트 폴더 경로로 변경하세요)

3. **패키지 설치**
   ```cmd
   pip install -r requirements.txt
   ```

### 설치 확인

설치가 완료되면 다음과 같은 메시지가 나옵니다:
```
Successfully installed requests-2.31.0 python-dotenv-1.0.0 ...
```

---

## 4. API 키 설정

### GUI로 설정 (추천! 🎨)

1. **설정 프로그램 실행**
   ```cmd
   python config_gui.py
   ```

2. **설정 창에서 입력**
   - App Key: 키움증권에서 발급받은 앱 키
   - App Secret: 키움증권에서 발급받은 시크릿
   - 계좌번호: 본인의 계좌번호 (10자리)
   - 거래 환경: **모의투자** 선택 (처음엔 꼭!)

3. **저장 및 테스트**
   - "💾 설정 저장" 버튼 클릭
   - "🔌 연결 테스트" 버튼으로 확인

---

## 5. 프로그램 실행

### GUI 버전 실행 (추천! 🖥️)

```cmd
python main_gui.py
```

**GUI 화면에서:**
- 🔌 "연결" 버튼 클릭
- 계좌 정보 자동으로 표시됨
- 보유 종목 확인
- 시세 조회 가능

### CLI 버전 실행

```cmd
python main.py
```

메뉴에서 원하는 기능 선택

---

## 💡 전체 과정 요약 (Windows)

```cmd
# 1. 프로젝트 폴더로 이동
cd C:\Users\사용자이름\다운로드\stock

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 설정 (GUI)
python config_gui.py

# 4. 프로그램 실행 (GUI)
python main_gui.py
```

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: "python을 찾을 수 없습니다" 오류가 나요
**A:** Python이 설치되지 않았거나 환경변수 설정이 안 됨
- Python 재설치 시 "Add Python to PATH" 체크!

### Q2: pip 명령어가 안 먹혀요
**A:** 다음 명령어 시도:
```cmd
python -m pip install -r requirements.txt
```

### Q3: 설치는 됐는데 실행이 안 돼요
**A:**
1. 프로젝트 폴더에 있는지 확인 (`dir` 명령어로 파일 목록 확인)
2. `config_gui.py` 파일이 보이면 올바른 폴더

### Q4: API 키는 어디서 받나요?
**A:**
1. 키움증권 홈페이지 접속
2. OpenAPI → REST API 메뉴
3. 앱 키 발급 신청
4. 승인 후 발급

### Q5: 모의투자와 실거래 차이는?
**A:**
- **모의투자**: 가상 돈으로 연습 (안전!)
- **실거래**: 실제 돈으로 거래 (위험!)
- **반드시 모의투자로 충분히 테스트 후 실거래 사용!**

---

## 🆘 문제 해결

### 방법 1: 관리자 권한으로 실행
1. 명령 프롬프트를 **관리자 권한**으로 실행
2. 패키지 재설치

### 방법 2: 가상환경 사용
```cmd
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 방법 3: 특정 패키지만 설치
```cmd
pip install requests
pip install python-dotenv
pip install pandas
pip install numpy
pip install colorlog
```

---

## ⚠️ 주의사항

1. **처음엔 꼭 모의투자로!**
2. 자동매매는 손실 위험이 있습니다
3. API 키는 절대 공유하지 마세요
4. .env 파일은 Git에 올리지 마세요

---

## 📞 도움이 필요하면

- 오류 메시지를 정확히 복사해서 문의하세요
- 어느 단계에서 막혔는지 알려주세요
- 스크린샷이 있으면 더 좋습니다!

즐거운 자동매매 되세요! 🚀
