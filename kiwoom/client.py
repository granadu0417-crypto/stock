"""키움증권 REST API 클라이언트"""
import requests
from typing import Dict, Any, Optional
from config import Config
from utils import setup_logger


class KiwoomAPIClient:
    """키움증권 REST API 기본 클라이언트 클래스"""

    def __init__(self):
        """클라이언트 초기화"""
        self.logger = setup_logger(__name__)
        self.base_url = Config.get_base_url()
        self.app_key = Config.KIWOOM_APP_KEY
        self.app_secret = Config.KIWOOM_APP_SECRET
        self.access_token: Optional[str] = None
        self.session = requests.Session()

        self.logger.info(f"키움증권 API 클라이언트 초기화 (환경: {Config.KIWOOM_ENVIRONMENT})")

    def _get_headers(self, tr_id: str, is_post: bool = False) -> Dict[str, str]:
        """API 요청 헤더 생성

        Args:
            tr_id: 거래ID (TR_ID)
            is_post: POST 요청 여부

        Returns:
            요청 헤더 딕셔너리
        """
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.access_token}" if self.access_token else "",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id,
        }
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        tr_id: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """API 요청 실행

        Args:
            method: HTTP 메서드 (GET, POST 등)
            endpoint: API 엔드포인트
            tr_id: 거래ID
            params: 쿼리 파라미터
            data: 요청 바디 데이터

        Returns:
            API 응답 딕셔너리

        Raises:
            requests.exceptions.RequestException: API 요청 실패 시
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(tr_id, is_post=(method == "POST"))

        self.logger.debug(f"{method} {url}")
        self.logger.debug(f"TR_ID: {tr_id}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            # 응답 코드 확인
            rt_cd = result.get("rt_cd", "")
            msg1 = result.get("msg1", "")

            if rt_cd != "0":
                self.logger.error(f"API 오류: [{rt_cd}] {msg1}")
                raise Exception(f"API 오류: [{rt_cd}] {msg1}")

            self.logger.debug(f"API 응답: {msg1}")
            return result

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API 요청 실패: {e}")
            raise

    def get(
        self,
        endpoint: str,
        tr_id: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """GET 요청

        Args:
            endpoint: API 엔드포인트
            tr_id: 거래ID
            params: 쿼리 파라미터

        Returns:
            API 응답
        """
        return self._request("GET", endpoint, tr_id, params=params)

    def post(
        self,
        endpoint: str,
        tr_id: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """POST 요청

        Args:
            endpoint: API 엔드포인트
            tr_id: 거래ID
            data: 요청 바디

        Returns:
            API 응답
        """
        return self._request("POST", endpoint, tr_id, data=data)

    def close(self):
        """세션 종료"""
        self.session.close()
        self.logger.info("API 클라이언트 종료")
