# 키움증권 REST API 자동매매 프로그램

키움증권의 REST API를 활용한 주식 자동매매 시스템입니다.

## 주요 기능

- 🔐 키움증권 REST API 인증 및 토큰 관리
- 💰 계좌 정보 및 잔고 조회
- 📊 실시간 시세 조회
- 📈 주문 기능 (매수/매도/정정/취소)
- 🤖 자동매매 전략 프레임워크
- 📝 상세한 로깅 및 에러 처리
- 🖥️ GUI 인터페이스 (설정 및 메인 화면)

## 프로젝트 구조

```
stock/
├── README.md                # 프로젝트 설명
├── requirements.txt         # Python 패키지 의존성
├── .gitignore              # Git 제외 파일
├── .env.example            # 환경변수 예제
├── config_gui.py           # GUI 설정 프로그램
├── main_gui.py             # GUI 메인 프로그램
├── main.py                 # CLI 메인 프로그램
├── config/
│   └── config.py           # 설정 파일
├── kiwoom/
│   ├── __init__.py
│   ├── client.py           # REST API 클라이언트
│   ├── auth.py             # 인증 처리
│   ├── account.py          # 계좌 관련 기능
│   ├── market.py           # 시세 조회 기능
│   └── order.py            # 주문 기능
├── strategy/
│   ├── __init__.py
│   ├── base_strategy.py    # 전략 베이스 클래스
│   └── simple_strategy.py  # 이동평균 전략 예제
└── utils/
    ├── __init__.py
    └── logger.py           # 로깅 유틸
```

## 시작하기

### 1. 사전 요구사항

- Python 3.8 이상
- 키움증권 계좌 및 REST API 접근 권한
- App Key 및 App Secret (키움증권에서 발급)

### 2. 설치

```bash
# 저장소 클론
git clone <repository-url>
cd stock

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 설정

#### GUI로 설정 (추천! 🎨)

```bash
python config_gui.py
```

GUI 화면에서 App Key, App Secret, 계좌번호를 입력하고 저장하세요.

#### 또는 수동 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 정보를 입력합니다.

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_APP_SECRET=your_app_secret_here
KIWOOM_ACCOUNT_NUMBER=your_account_number_here
```

### 4. 실행

#### GUI 버전 (추천! 🖥️)

```bash
python main_gui.py
```

#### CLI 버전

```bash
python main.py
```

## 키움증권 REST API 발급 방법

1. 키움증권 홈페이지 접속
2. OpenAPI > REST API 메뉴 선택
3. App Key 및 App Secret 발급 신청
4. 승인 후 발급된 키 정보를 `.env` 파일에 입력

## 주의사항

⚠️ **실제 거래 전 모의투자로 충분히 테스트하세요!**

- 자동매매는 손실 위험이 있습니다
- 본인의 투자 판단과 책임 하에 사용하세요
- API 키와 계좌 정보는 절대 공유하지 마세요
- `.env` 파일은 Git에 커밋하지 마세요

## 라이선스

MIT License

## 기여

이슈와 풀 리퀘스트는 언제나 환영합니다!
