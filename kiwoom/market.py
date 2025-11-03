"""키움증권 시세 조회 기능"""
from typing import Dict, Any, List
from kiwoom.auth import KiwoomAuth
from config import Config
from utils import setup_logger


class KiwoomMarket(KiwoomAuth):
    """시세 조회 클래스"""

    def __init__(self):
        """시세 조회 클라이언트 초기화"""
        super().__init__()
        self.logger = setup_logger(__name__)

    def get_current_price(self, stock_code: str) -> Dict[str, Any]:
        """현재가 조회

        Args:
            stock_code: 종목코드 (6자리)

        Returns:
            현재가 정보 딕셔너리
            - 현재가, 전일대비, 등락률, 거래량, 시가, 고가, 저가 등
        """
        self.ensure_token()
        self.logger.info(f"현재가 조회: {stock_code}")

        endpoint = "/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 구분 (J: 주식)
            "FID_INPUT_ISCD": stock_code,  # 종목코드
        }

        try:
            result = self.get(endpoint, tr_id, params)
            output = result.get("output", {})

            price_info = {
                "종목코드": stock_code,
                "종목명": output.get("prdt_name", ""),
                "현재가": int(output.get("stck_prpr", 0)),
                "전일대비": int(output.get("prdy_vrss", 0)),
                "등락률": float(output.get("prdy_ctrt", 0)),
                "시가": int(output.get("stck_oprc", 0)),
                "고가": int(output.get("stck_hgpr", 0)),
                "저가": int(output.get("stck_lwpr", 0)),
                "거래량": int(output.get("acml_vol", 0)),
                "거래대금": int(output.get("acml_tr_pbmn", 0)),
            }

            self.logger.info(
                f"{price_info['종목명']} 현재가: {price_info['현재가']:,}원 "
                f"({price_info['등락률']:+.2f}%)"
            )
            return price_info

        except Exception as e:
            self.logger.error(f"현재가 조회 실패: {e}")
            raise

    def get_daily_price(
        self, stock_code: str, period: str = "D"
    ) -> List[Dict[str, Any]]:
        """일봉/주봉/월봉 데이터 조회

        Args:
            stock_code: 종목코드 (6자리)
            period: 기간 구분 (D: 일봉, W: 주봉, M: 월봉)

        Returns:
            OHLCV 데이터 리스트 (최대 100개)
        """
        self.ensure_token()
        self.logger.info(f"일봉 데이터 조회: {stock_code}")

        endpoint = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"
        tr_id = "FHKST01010400"

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
            "FID_PERIOD_DIV_CODE": period,  # D: 일, W: 주, M: 월
            "FID_ORG_ADJ_PRC": "0",  # 수정주가 구분 (0: 수정주가 반영)
        }

        try:
            result = self.get(endpoint, tr_id, params)
            output_list = result.get("output", [])

            price_data = []
            for item in output_list:
                data = {
                    "일자": item.get("stck_bsop_date", ""),
                    "시가": int(item.get("stck_oprc", 0)),
                    "고가": int(item.get("stck_hgpr", 0)),
                    "저가": int(item.get("stck_lwpr", 0)),
                    "종가": int(item.get("stck_clpr", 0)),
                    "거래량": int(item.get("acml_vol", 0)),
                }
                price_data.append(data)

            self.logger.info(f"일봉 데이터 {len(price_data)}개 조회 완료")
            return price_data

        except Exception as e:
            self.logger.error(f"일봉 데이터 조회 실패: {e}")
            raise

    def search_stock(self, keyword: str) -> List[Dict[str, Any]]:
        """종목 검색

        Args:
            keyword: 검색 키워드 (종목명 또는 종목코드)

        Returns:
            검색 결과 리스트
        """
        self.ensure_token()
        self.logger.info(f"종목 검색: {keyword}")

        endpoint = "/uapi/domestic-stock/v1/quotations/search-stock-info"
        tr_id = "CTPF1604R"

        params = {
            "PRDT_TYPE_CD": "300",  # 상품유형코드 (300: 주식)
            "PDNO": keyword,  # 검색어
        }

        try:
            result = self.get(endpoint, tr_id, params)
            output_list = result.get("output", [])

            stocks = []
            for item in output_list:
                stock_info = {
                    "종목코드": item.get("pdno", ""),
                    "종목명": item.get("prdt_name", ""),
                    "시장구분": item.get("prdt_abrv_name", ""),
                }
                stocks.append(stock_info)

            self.logger.info(f"검색 결과 {len(stocks)}개 발견")
            return stocks

        except Exception as e:
            self.logger.error(f"종목 검색 실패: {e}")
            raise

    def get_market_index(self, market_code: str = "0001") -> Dict[str, Any]:
        """시장 지수 조회

        Args:
            market_code: 시장코드
                - 0001: 코스피
                - 1001: 코스닥
                - 2001: 코스피200

        Returns:
            시장 지수 정보
        """
        self.ensure_token()
        self.logger.info(f"시장 지수 조회: {market_code}")

        endpoint = "/uapi/domestic-stock/v1/quotations/inquire-index-price"
        tr_id = "FHKUP03500100"

        params = {
            "FID_COND_MRKT_DIV_CODE": "U",
            "FID_INPUT_ISCD": market_code,
        }

        try:
            result = self.get(endpoint, tr_id, params)
            output = result.get("output", {})

            index_info = {
                "지수명": "코스피" if market_code == "0001" else "코스닥",
                "현재지수": float(output.get("bstp_nmix_prpr", 0)),
                "전일대비": float(output.get("bstp_nmix_prdy_vrss", 0)),
                "등락률": float(output.get("prdy_vrss_sign", 0)),
                "거래량": int(output.get("acml_vol", 0)),
                "거래대금": int(output.get("acml_tr_pbmn", 0)),
            }

            self.logger.info(
                f"{index_info['지수명']} 지수: {index_info['현재지수']:.2f} "
                f"({index_info['전일대비']:+.2f})"
            )
            return index_info

        except Exception as e:
            self.logger.error(f"시장 지수 조회 실패: {e}")
            raise
