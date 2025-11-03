"""간단한 예제 전략 - 이동평균 교차 전략"""
from typing import Dict, Any, List
from strategy.base_strategy import BaseStrategy


class SimpleMovingAverageStrategy(BaseStrategy):
    """단순 이동평균 교차 전략

    단기 이동평균이 장기 이동평균을 상향 돌파하면 매수
    단기 이동평균이 장기 이동평균을 하향 돌파하면 매도
    """

    def __init__(
        self,
        watchlist: List[str],
        short_period: int = 5,
        long_period: int = 20,
        quantity: int = 1,
    ):
        """전략 초기화

        Args:
            watchlist: 관심 종목 리스트
            short_period: 단기 이동평균 기간 (일)
            long_period: 장기 이동평균 기간 (일)
            quantity: 매수/매도 수량
        """
        super().__init__(name="이동평균교차전략")
        self.watchlist = watchlist
        self.short_period = short_period
        self.long_period = long_period
        self.quantity = quantity

    def get_watchlist(self) -> List[str]:
        """관심 종목 리스트 반환"""
        return self.watchlist

    def calculate_moving_average(self, prices: List[int], period: int) -> float:
        """이동평균 계산

        Args:
            prices: 가격 리스트
            period: 이동평균 기간

        Returns:
            이동평균 값
        """
        if len(prices) < period:
            return 0.0
        return sum(prices[:period]) / period

    def analyze(self, stock_code: str) -> Dict[str, Any]:
        """종목 분석"""
        try:
            # 일봉 데이터 조회
            daily_prices = self.market.get_daily_price(stock_code, period="D")

            if len(daily_prices) < self.long_period:
                return {
                    "signal": "hold",
                    "reason": "데이터 부족",
                }

            # 종가 리스트 추출
            closing_prices = [p["종가"] for p in daily_prices]

            # 이동평균 계산
            short_ma = self.calculate_moving_average(
                closing_prices, self.short_period
            )
            long_ma = self.calculate_moving_average(closing_prices, self.long_period)

            # 이전 이동평균 계산 (교차 감지용)
            prev_short_ma = self.calculate_moving_average(
                closing_prices[1:], self.short_period
            )
            prev_long_ma = self.calculate_moving_average(
                closing_prices[1:], self.long_period
            )

            self.logger.debug(
                f"{stock_code} MA({self.short_period}): {short_ma:.2f}, "
                f"MA({self.long_period}): {long_ma:.2f}"
            )

            # 골든 크로스 (매수 신호)
            if prev_short_ma <= prev_long_ma and short_ma > long_ma:
                return {
                    "signal": "buy",
                    "reason": f"골든크로스 발생 (MA{self.short_period} > MA{self.long_period})",
                    "quantity": self.quantity,
                }

            # 데드 크로스 (매도 신호)
            elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
                return {
                    "signal": "sell",
                    "reason": f"데드크로스 발생 (MA{self.short_period} < MA{self.long_period})",
                    "quantity": self.quantity,
                }

            else:
                return {
                    "signal": "hold",
                    "reason": "조건 미충족",
                }

        except Exception as e:
            self.logger.error(f"분석 중 오류: {e}")
            return {
                "signal": "hold",
                "reason": f"오류: {e}",
            }

    def should_buy(self, stock_code: str) -> bool:
        """매수 조건 판단"""
        analysis = self.analyze(stock_code)
        return analysis.get("signal") == "buy"

    def should_sell(self, stock_code: str) -> bool:
        """매도 조건 판단"""
        analysis = self.analyze(stock_code)
        return analysis.get("signal") == "sell"
