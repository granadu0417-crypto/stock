"""키움증권 주문 기능"""
from typing import Dict, Any
from kiwoom.auth import KiwoomAuth
from config import Config
from utils import setup_logger


class KiwoomOrder(KiwoomAuth):
    """주식 주문 클래스"""

    def __init__(self):
        """주문 클라이언트 초기화"""
        super().__init__()
        self.logger = setup_logger(__name__)
        self.account_number = Config.KIWOOM_ACCOUNT_NUMBER

    def buy_market_order(self, stock_code: str, quantity: int) -> Dict[str, Any]:
        """시장가 매수 주문

        Args:
            stock_code: 종목코드 (6자리)
            quantity: 매수 수량

        Returns:
            주문 결과 딕셔너리
        """
        return self._place_order(
            stock_code=stock_code,
            quantity=quantity,
            price=0,
            order_type="01",  # 시장가
            side="buy",
        )

    def buy_limit_order(
        self, stock_code: str, quantity: int, price: int
    ) -> Dict[str, Any]:
        """지정가 매수 주문

        Args:
            stock_code: 종목코드
            quantity: 매수 수량
            price: 매수 가격

        Returns:
            주문 결과 딕셔너리
        """
        return self._place_order(
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            order_type="00",  # 지정가
            side="buy",
        )

    def sell_market_order(self, stock_code: str, quantity: int) -> Dict[str, Any]:
        """시장가 매도 주문

        Args:
            stock_code: 종목코드
            quantity: 매도 수량

        Returns:
            주문 결과 딕셔너리
        """
        return self._place_order(
            stock_code=stock_code,
            quantity=quantity,
            price=0,
            order_type="01",  # 시장가
            side="sell",
        )

    def sell_limit_order(
        self, stock_code: str, quantity: int, price: int
    ) -> Dict[str, Any]:
        """지정가 매도 주문

        Args:
            stock_code: 종목코드
            quantity: 매도 수량
            price: 매도 가격

        Returns:
            주문 결과 딕셔너리
        """
        return self._place_order(
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            order_type="00",  # 지정가
            side="sell",
        )

    def _place_order(
        self,
        stock_code: str,
        quantity: int,
        price: int,
        order_type: str,
        side: str,
    ) -> Dict[str, Any]:
        """주문 실행 (내부 메서드)

        Args:
            stock_code: 종목코드
            quantity: 주문 수량
            price: 주문 가격 (시장가는 0)
            order_type: 주문 유형 (00: 지정가, 01: 시장가)
            side: 매수/매도 구분 (buy/sell)

        Returns:
            주문 결과
        """
        self.ensure_token()

        endpoint = "/uapi/domestic-stock/v1/trading/order-cash"

        # 모의투자와 실거래의 TR_ID가 다름
        if Config.KIWOOM_ENVIRONMENT == "real":
            tr_id = "TTTC0802U" if side == "buy" else "TTTC0801U"
        else:
            tr_id = "VTTC0802U" if side == "buy" else "VTTC0801U"

        order_data = {
            "CANO": self.account_number[:8],  # 계좌번호 앞 8자리
            "ACNT_PRDT_CD": self.account_number[8:],  # 계좌번호 뒤 2자리
            "PDNO": stock_code,  # 종목코드
            "ORD_DVSN": order_type,  # 주문구분
            "ORD_QTY": str(quantity),  # 주문수량
            "ORD_UNPR": str(price),  # 주문단가
        }

        # 해시키 발급
        hash_key = self.get_hash_key(order_data)

        self.logger.info(
            f"{'매수' if side == 'buy' else '매도'} 주문: "
            f"{stock_code} {quantity}주 "
            f"{'시장가' if order_type == '01' else f'{price:,}원'}"
        )

        try:
            # 주문 헤더에 해시키 추가
            headers = self._get_headers(tr_id, is_post=True)
            headers["hashkey"] = hash_key

            response = self.session.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                json=order_data,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            # 응답 코드 확인
            rt_cd = result.get("rt_cd", "")
            msg1 = result.get("msg1", "")

            if rt_cd != "0":
                self.logger.error(f"주문 실패: [{rt_cd}] {msg1}")
                raise Exception(f"주문 실패: [{rt_cd}] {msg1}")

            output = result.get("output", {})
            order_result = {
                "주문번호": output.get("ODNO", ""),
                "주문시각": output.get("ORD_TMD", ""),
                "메시지": msg1,
            }

            self.logger.info(f"주문 성공: {msg1} (주문번호: {order_result['주문번호']})")
            return order_result

        except Exception as e:
            self.logger.error(f"주문 실행 실패: {e}")
            raise

    def cancel_order(self, order_number: str, quantity: int, stock_code: str) -> Dict[str, Any]:
        """주문 취소

        Args:
            order_number: 원주문번호
            quantity: 취소 수량
            stock_code: 종목코드

        Returns:
            취소 결과
        """
        self.ensure_token()

        endpoint = "/uapi/domestic-stock/v1/trading/order-rvsecncl"

        if Config.KIWOOM_ENVIRONMENT == "real":
            tr_id = "TTTC0803U"
        else:
            tr_id = "VTTC0803U"

        cancel_data = {
            "CANO": self.account_number[:8],
            "ACNT_PRDT_CD": self.account_number[8:],
            "KRX_FWDG_ORD_ORGNO": "",  # 한국거래소전송주문조직번호
            "ORGN_ODNO": order_number,  # 원주문번호
            "ORD_DVSN": "00",  # 주문구분 (00: 지정가)
            "RVSE_CNCL_DVSN_CD": "02",  # 정정취소구분 (02: 취소)
            "ORD_QTY": "0",  # 주문수량 (취소시 0)
            "ORD_UNPR": "0",  # 주문단가 (취소시 0)
            "QTY_ALL_ORD_YN": "Y",  # 전량주문여부 (Y: 전량)
        }

        hash_key = self.get_hash_key(cancel_data)

        self.logger.info(f"주문 취소: {order_number}")

        try:
            headers = self._get_headers(tr_id, is_post=True)
            headers["hashkey"] = hash_key

            response = self.session.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                json=cancel_data,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            rt_cd = result.get("rt_cd", "")
            msg1 = result.get("msg1", "")

            if rt_cd != "0":
                self.logger.error(f"주문 취소 실패: [{rt_cd}] {msg1}")
                raise Exception(f"주문 취소 실패: [{rt_cd}] {msg1}")

            self.logger.info(f"주문 취소 성공: {msg1}")
            return {"메시지": msg1}

        except Exception as e:
            self.logger.error(f"주문 취소 실패: {e}")
            raise

    def modify_order(
        self,
        order_number: str,
        stock_code: str,
        quantity: int,
        price: int,
    ) -> Dict[str, Any]:
        """주문 정정

        Args:
            order_number: 원주문번호
            stock_code: 종목코드
            quantity: 정정 수량
            price: 정정 가격

        Returns:
            정정 결과
        """
        self.ensure_token()

        endpoint = "/uapi/domestic-stock/v1/trading/order-rvsecncl"

        if Config.KIWOOM_ENVIRONMENT == "real":
            tr_id = "TTTC0803U"
        else:
            tr_id = "VTTC0803U"

        modify_data = {
            "CANO": self.account_number[:8],
            "ACNT_PRDT_CD": self.account_number[8:],
            "KRX_FWDG_ORD_ORGNO": "",
            "ORGN_ODNO": order_number,
            "ORD_DVSN": "00",  # 지정가
            "RVSE_CNCL_DVSN_CD": "01",  # 정정취소구분 (01: 정정)
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price),
            "QTY_ALL_ORD_YN": "N",
        }

        hash_key = self.get_hash_key(modify_data)

        self.logger.info(f"주문 정정: {order_number} -> {quantity}주 {price:,}원")

        try:
            headers = self._get_headers(tr_id, is_post=True)
            headers["hashkey"] = hash_key

            response = self.session.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                json=modify_data,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            rt_cd = result.get("rt_cd", "")
            msg1 = result.get("msg1", "")

            if rt_cd != "0":
                self.logger.error(f"주문 정정 실패: [{rt_cd}] {msg1}")
                raise Exception(f"주문 정정 실패: [{rt_cd}] {msg1}")

            self.logger.info(f"주문 정정 성공: {msg1}")
            return {"메시지": msg1}

        except Exception as e:
            self.logger.error(f"주문 정정 실패: {e}")
            raise
