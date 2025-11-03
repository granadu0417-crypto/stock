"""프로젝트 설정 관리"""
import os
from typing import Optional
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """애플리케이션 설정 클래스"""

    # 키움증권 API 설정
    KIWOOM_APP_KEY: str = os.getenv('KIWOOM_APP_KEY', '')
    KIWOOM_APP_SECRET: str = os.getenv('KIWOOM_APP_SECRET', '')
    KIWOOM_ACCOUNT_NUMBER: str = os.getenv('KIWOOM_ACCOUNT_NUMBER', '')

    # API 환경 (real: 실거래, mock: 모의투자)
    KIWOOM_ENVIRONMENT: str = os.getenv('KIWOOM_ENVIRONMENT', 'mock')

    # 키움증권 REST API 엔드포인트
    KIWOOM_BASE_URL: str = 'https://openapi.koreainvestment.com:9443'  # 실서버
    KIWOOM_MOCK_URL: str = 'https://openapivts.koreainvestment.com:29443'  # 모의투자

    # 로깅 설정
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def get_base_url(cls) -> str:
        """환경에 따른 API 베이스 URL 반환"""
        if cls.KIWOOM_ENVIRONMENT == 'real':
            return cls.KIWOOM_BASE_URL
        return cls.KIWOOM_MOCK_URL

    @classmethod
    def validate(cls) -> bool:
        """필수 설정 값 검증"""
        if not cls.KIWOOM_APP_KEY:
            raise ValueError("KIWOOM_APP_KEY가 설정되지 않았습니다.")
        if not cls.KIWOOM_APP_SECRET:
            raise ValueError("KIWOOM_APP_SECRET이 설정되지 않았습니다.")
        if not cls.KIWOOM_ACCOUNT_NUMBER:
            raise ValueError("KIWOOM_ACCOUNT_NUMBER가 설정되지 않았습니다.")
        return True
