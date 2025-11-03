"""키움증권 API 인증 관리"""
import hashlib
import time
from typing import Optional
from datetime import datetime
from kiwoom.client import KiwoomAPIClient
from utils import setup_logger


class KiwoomAuth(KiwoomAPIClient):
    """키움증권 API 인증 클래스"""

    def __init__(self):
        """인증 클라이언트 초기화"""
        super().__init__()
        self.logger = setup_logger(__name__)
        self.token_expire_time: Optional[float] = None

    def get_access_token(self) -> str:
        """접근 토큰 발급

        Returns:
            접근 토큰 문자열

        Raises:
            Exception: 토큰 발급 실패 시
        """
        self.logger.info("접근 토큰 발급 시작")

        endpoint = "/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.secret_key,
        }

        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json;charset=UTF-8"},
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            # 키움증권 응답 체크
            return_code = result.get("return_code", -1)
            return_msg = result.get("return_msg", "")

            if return_code != 0:
                raise Exception(f"토큰 발급 실패: [{return_code}] {return_msg}")

            # 토큰 정보 추출
            self.access_token = result.get("token")
            expires_dt = result.get("expires_dt", "")  # 예: "20241107083713"

            if not self.access_token:
                raise Exception("접근 토큰을 받지 못했습니다.")

            # 만료 시간 계산 (expires_dt를 timestamp로 변환)
            if expires_dt:
                try:
                    expire_datetime = datetime.strptime(expires_dt, "%Y%m%d%H%M%S")
                    self.token_expire_time = expire_datetime.timestamp()
                except:
                    # 파싱 실패시 기본 24시간
                    self.token_expire_time = time.time() + 86400
            else:
                self.token_expire_time = time.time() + 86400

            self.logger.info(f"접근 토큰 발급 완료 (만료: {expires_dt})")
            return self.access_token

        except Exception as e:
            self.logger.error(f"접근 토큰 발급 실패: {e}")
            raise

    def is_token_valid(self) -> bool:
        """토큰 유효성 검사

        Returns:
            토큰이 유효하면 True, 아니면 False
        """
        if not self.access_token:
            return False

        if not self.token_expire_time:
            return False

        # 만료 5분 전에 갱신하도록 여유 시간 둠
        return time.time() < (self.token_expire_time - 300)

    def ensure_token(self):
        """토큰 확인 및 갱신

        토큰이 없거나 만료되었으면 새로 발급받습니다.
        """
        if not self.is_token_valid():
            self.logger.info("토큰이 없거나 만료되었습니다. 재발급합니다.")
            self.get_access_token()

    def get_hash_key(self, data: dict) -> str:
        """주문 등에 사용되는 해시키 발급

        Args:
            data: 주문 데이터

        Returns:
            해시키 문자열
        """
        self.ensure_token()

        endpoint = "/uapi/hashkey"

        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "appkey": self.app_key,
                    "appsecret": self.app_secret,
                },
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            hash_key = result.get("HASH")
            if not hash_key:
                raise Exception("해시키를 받지 못했습니다.")

            self.logger.debug("해시키 발급 완료")
            return hash_key

        except Exception as e:
            self.logger.error(f"해시키 발급 실패: {e}")
            raise
