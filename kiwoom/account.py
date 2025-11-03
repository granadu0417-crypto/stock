"""키움증권 계좌 관련 기능"""
from typing import Dict, Any, List
from kiwoom.auth import KiwoomAuth
from config import Config
from utils import setup_logger


class KiwoomAccount(KiwoomAuth):
    """계좌 조회 및 관리 클래스"""

    def __init__(self):
        """계좌 클라이언트 초기화"""
        super().__init__()
        self.logger = setup_logger(__name__)
        self.account_number = Config.KIWOOM_ACCOUNT_NUMBER

    def get_balance(self) -> Dict[str, Any]:
        """계좌 잔고 조회

        Returns:
            계좌 잔고 정보 딕셔너리
            - 예수금 (주문가능현금)
            - 총평가금액
            - 총손익
            - 수익률
        """
        self.ensure_token()
        self.logger.info(f"계좌 잔고 조회: {self.account_number}")

        endpoint = "/uapi/domestic-stock/v1/trading/inquire-psbl-order"
        tr_id = "TTTC8908R"  # 모의투자용

        if Config.KIWOOM_ENVIRONMENT == "real":
            tr_id = "TTTC8908R"  # 실거래용 TR_ID (동일)

        params = {
            "CANO": self.account_number[:8],  # 계좌번호 앞 8자리
            "ACNT_PRDT_CD": self.account_number[8:],  # 계좌번호 뒤 2자리
            "PDNO": "",  # 종목번호 (전체 조회시 공백)
            "ORD_UNPR": "",  # 주문단가
            "ORD_DVSN": "01",  # 주문구분 (01: 시장가)
            "CMA_EVLU_AMT_ICLD_YN": "Y",  # CMA평가금액 포함여부
            "OVRS_ICLD_YN": "N",  # 해외포함여부
        }

        try:
            result = self.get(endpoint, tr_id, params)
            output = result.get("output", {})

            balance_info = {
                "예수금": int(output.get("ord_psbl_cash", 0)),  # 주문가능현금
                "총매입금액": int(output.get("pchs_amt_smtl", 0)),  # 매입금액합계
                "총평가금액": int(output.get("evlu_amt_smtl", 0)),  # 평가금액합계
                "총손익": int(output.get("evlu_pfls_smtl", 0)),  # 평가손익합계
                "수익률": float(output.get("evlu_pfls_rt", 0)),  # 수익률
            }

            self.logger.info(f"잔고 조회 완료: 예수금 {balance_info['예수금']:,}원")
            return balance_info

        except Exception as e:
            self.logger.error(f"잔고 조회 실패: {e}")
            raise

    def get_stock_balance(self) -> List[Dict[str, Any]]:
        """보유 주식 잔고 조회

        Returns:
            보유 주식 목록
            각 종목별로 종목코드, 종목명, 보유수량, 매입가, 현재가, 평가손익 등
        """
        self.ensure_token()
        self.logger.info("보유 주식 조회")

        endpoint = "/uapi/domestic-stock/v1/trading/inquire-balance"
        tr_id = "VTTC8434R"  # 모의투자용

        if Config.KIWOOM_ENVIRONMENT == "real":
            tr_id = "TTTC8434R"  # 실거래용

        params = {
            "CANO": self.account_number[:8],
            "ACNT_PRDT_CD": self.account_number[8:],
            "AFHR_FLPR_YN": "N",  # 시간외단일가여부
            "OFL_YN": "",  # 오프라인여부
            "INQR_DVSN": "02",  # 조회구분 (01: 대출일별, 02: 종목별)
            "UNPR_DVSN": "01",  # 단가구분
            "FUND_STTL_ICLD_YN": "N",  # 펀드결제분포함여부
            "FNCG_AMT_AUTO_RDPT_YN": "N",  # 융자금액자동상환여부
            "PRCS_DVSN": "01",  # 처리구분 (00: 전일, 01: 당일)
            "CTX_AREA_FK100": "",  # 연속조회검색조건
            "CTX_AREA_NK100": "",  # 연속조회키
        }

        try:
            result = self.get(endpoint, tr_id, params)
            output_list = result.get("output1", [])

            stocks = []
            for stock in output_list:
                stock_info = {
                    "종목코드": stock.get("pdno", ""),
                    "종목명": stock.get("prdt_name", ""),
                    "보유수량": int(stock.get("hldg_qty", 0)),
                    "매입평균가": int(stock.get("pchs_avg_pric", 0)),
                    "현재가": int(stock.get("prpr", 0)),
                    "평가금액": int(stock.get("evlu_amt", 0)),
                    "평가손익": int(stock.get("evlu_pfls_amt", 0)),
                    "수익률": float(stock.get("evlu_pfls_rt", 0)),
                }
                stocks.append(stock_info)

            self.logger.info(f"보유 주식 {len(stocks)}종목 조회 완료")
            return stocks

        except Exception as e:
            self.logger.error(f"보유 주식 조회 실패: {e}")
            raise

    def get_order_history(self) -> List[Dict[str, Any]]:
        """당일 주문 체결 내역 조회

        Returns:
            주문 체결 내역 리스트
        """
        self.ensure_token()
        self.logger.info("주문 체결 내역 조회")

        endpoint = "/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
        tr_id = "VTTC8001R"  # 모의투자용

        if Config.KIWOOM_ENVIRONMENT == "real":
            tr_id = "TTTC8001R"  # 실거래용

        params = {
            "CANO": self.account_number[:8],
            "ACNT_PRDT_CD": self.account_number[8:],
            "INQR_STRT_DT": "",  # 조회시작일자 (당일은 공백)
            "INQR_END_DT": "",  # 조회종료일자
            "SLL_BUY_DVSN_CD": "00",  # 매도매수구분 (00: 전체)
            "INQR_DVSN": "00",  # 조회구분 (00: 역순)
            "PDNO": "",  # 종목코드
            "CCLD_DVSN": "00",  # 체결구분 (00: 전체)
            "ORD_GNO_BRNO": "",  # 주문채번지점번호
            "ODNO": "",  # 주문번호
            "INQR_DVSN_3": "00",  # 조회구분3
            "INQR_DVSN_1": "",  # 조회구분1
            "CTX_AREA_FK100": "",  # 연속조회검색조건
            "CTX_AREA_NK100": "",  # 연속조회키
        }

        try:
            result = self.get(endpoint, tr_id, params)
            output_list = result.get("output1", [])

            orders = []
            for order in output_list:
                order_info = {
                    "주문번호": order.get("odno", ""),
                    "종목코드": order.get("pdno", ""),
                    "종목명": order.get("prdt_name", ""),
                    "매도매수구분": "매수" if order.get("sll_buy_dvsn_cd") == "02" else "매도",
                    "주문수량": int(order.get("ord_qty", 0)),
                    "주문가격": int(order.get("ord_unpr", 0)),
                    "체결수량": int(order.get("tot_ccld_qty", 0)),
                    "체결가격": int(order.get("avg_prvs", 0)),
                    "주문시각": order.get("ord_tmd", ""),
                    "주문상태": order.get("ord_dvsn_name", ""),
                }
                orders.append(order_info)

            self.logger.info(f"주문 내역 {len(orders)}건 조회 완료")
            return orders

        except Exception as e:
            self.logger.error(f"주문 내역 조회 실패: {e}")
            raise
