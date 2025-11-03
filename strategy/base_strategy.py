"""자동매매 전략 베이스 클래스"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from kiwoom.market import KiwoomMarket
from kiwoom.account import KiwoomAccount
from kiwoom.order import KiwoomOrder
from utils import setup_logger


class BaseStrategy(ABC):
    """자동매매 전략 추상 클래스

    이 클래스를 상속받아 자신만의 전략을 구현할 수 있습니다.
    """

    def __init__(self, name: str = "기본전략"):
        """전략 초기화

        Args:
            name: 전략 이름
        """
        self.name = name
        self.logger = setup_logger(f"Strategy.{name}")

        # API 클라이언트 초기화
        self.market = KiwoomMarket()
        self.account = KiwoomAccount()
        self.order = KiwoomOrder()

        # 토큰 발급
        self.market.get_access_token()

        self.logger.info(f"전략 '{name}' 초기화 완료")

    @abstractmethod
    def analyze(self, stock_code: str) -> Dict[str, Any]:
        """종목 분석

        Args:
            stock_code: 분석할 종목코드

        Returns:
            분석 결과 딕셔너리
            - signal: 'buy', 'sell', 'hold' 중 하나
            - reason: 시그널 발생 이유
            - quantity: 매수/매도 수량 (선택사항)
            - price: 주문 가격 (선택사항, 없으면 시장가)
        """
        pass

    @abstractmethod
    def should_buy(self, stock_code: str) -> bool:
        """매수 조건 판단

        Args:
            stock_code: 종목코드

        Returns:
            매수해야 하면 True, 아니면 False
        """
        pass

    @abstractmethod
    def should_sell(self, stock_code: str) -> bool:
        """매도 조건 판단

        Args:
            stock_code: 종목코드

        Returns:
            매도해야 하면 True, 아니면 False
        """
        pass

    def execute_trade(self, stock_code: str):
        """매매 실행

        분석 결과에 따라 실제 주문을 실행합니다.

        Args:
            stock_code: 종목코드
        """
        try:
            # 종목 분석
            analysis = self.analyze(stock_code)
            signal = analysis.get("signal", "hold")
            reason = analysis.get("reason", "")

            self.logger.info(f"{stock_code} 분석 결과: {signal} - {reason}")

            if signal == "buy":
                quantity = analysis.get("quantity", 1)
                price = analysis.get("price")

                if price:
                    result = self.order.buy_limit_order(stock_code, quantity, price)
                else:
                    result = self.order.buy_market_order(stock_code, quantity)

                self.logger.info(f"매수 주문 완료: {result}")

            elif signal == "sell":
                quantity = analysis.get("quantity", 1)
                price = analysis.get("price")

                if price:
                    result = self.order.sell_limit_order(stock_code, quantity, price)
                else:
                    result = self.order.sell_market_order(stock_code, quantity)

                self.logger.info(f"매도 주문 완료: {result}")

            else:
                self.logger.info("관망 (주문 없음)")

        except Exception as e:
            self.logger.error(f"매매 실행 중 오류: {e}")

    def get_watchlist(self) -> List[str]:
        """관심 종목 리스트 반환

        Returns:
            종목코드 리스트
        """
        # 기본값으로 빈 리스트 반환
        # 하위 클래스에서 오버라이드하여 사용
        return []

    def run(self):
        """전략 실행

        관심 종목들을 순회하며 매매를 실행합니다.
        """
        self.logger.info(f"전략 '{self.name}' 실행 시작")

        watchlist = self.get_watchlist()
        if not watchlist:
            self.logger.warning("관심 종목이 없습니다.")
            return

        for stock_code in watchlist:
            try:
                self.execute_trade(stock_code)
            except Exception as e:
                self.logger.error(f"{stock_code} 처리 중 오류: {e}")
                continue

        self.logger.info(f"전략 '{self.name}' 실행 완료")

    def close(self):
        """리소스 정리"""
        self.market.close()
        self.account.close()
        self.order.close()
        self.logger.info("전략 종료")
