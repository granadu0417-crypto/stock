"""키움증권 자동매매 프로그램 메인"""
import sys
from config import Config
from utils import setup_logger
from kiwoom.account import KiwoomAccount
from kiwoom.market import KiwoomMarket
from strategy.simple_strategy import SimpleMovingAverageStrategy


def test_connection():
    """API 연결 테스트"""
    logger = setup_logger("main")
    logger.info("=" * 50)
    logger.info("키움증권 REST API 연결 테스트")
    logger.info("=" * 50)

    try:
        # 설정 검증
        Config.validate()
        logger.info("설정 검증 완료")

        # 계좌 클라이언트 생성 및 토큰 발급
        account = KiwoomAccount()
        account.get_access_token()
        logger.info("토큰 발급 완료")

        # 계좌 잔고 조회
        balance = account.get_balance()
        logger.info(f"계좌 잔고: {balance['예수금']:,}원")

        # 시장 지수 조회
        market = KiwoomMarket()
        market.access_token = account.access_token
        kospi = market.get_market_index("0001")
        logger.info(f"코스피 지수: {kospi['현재지수']:.2f}")

        logger.info("연결 테스트 성공!")
        return True

    except Exception as e:
        logger.error(f"연결 테스트 실패: {e}")
        return False


def run_strategy():
    """자동매매 전략 실행"""
    logger = setup_logger("main")
    logger.info("=" * 50)
    logger.info("자동매매 전략 실행")
    logger.info("=" * 50)

    try:
        # 관심 종목 리스트 (예시)
        # 실제 사용시 원하는 종목코드로 변경하세요
        watchlist = [
            "005930",  # 삼성전자
            "000660",  # SK하이닉스
        ]

        # 전략 생성 및 실행
        strategy = SimpleMovingAverageStrategy(
            watchlist=watchlist,
            short_period=5,  # 5일 이동평균
            long_period=20,  # 20일 이동평균
            quantity=1,  # 1주씩 매매
        )

        # 전략 실행
        strategy.run()

        # 리소스 정리
        strategy.close()

        logger.info("전략 실행 완료")

    except Exception as e:
        logger.error(f"전략 실행 실패: {e}")


def show_menu():
    """메뉴 출력"""
    print("\n" + "=" * 50)
    print("키움증권 자동매매 프로그램")
    print("=" * 50)
    print("1. API 연결 테스트")
    print("2. 계좌 정보 조회")
    print("3. 시세 조회")
    print("4. 자동매매 전략 실행")
    print("0. 종료")
    print("=" * 50)


def show_account_info():
    """계좌 정보 조회"""
    logger = setup_logger("main")

    try:
        account = KiwoomAccount()
        account.get_access_token()

        # 잔고 조회
        balance = account.get_balance()
        print("\n[계좌 잔고]")
        for key, value in balance.items():
            if key == "수익률":
                print(f"{key}: {value:.2f}%")
            else:
                print(f"{key}: {value:,}원")

        # 보유 주식 조회
        stocks = account.get_stock_balance()
        if stocks:
            print("\n[보유 주식]")
            for stock in stocks:
                print(f"\n종목: {stock['종목명']} ({stock['종목코드']})")
                print(f"  보유수량: {stock['보유수량']}주")
                print(f"  매입가: {stock['매입평균가']:,}원")
                print(f"  현재가: {stock['현재가']:,}원")
                print(f"  평가손익: {stock['평가손익']:,}원 ({stock['수익률']:+.2f}%)")
        else:
            print("\n보유 주식이 없습니다.")

        account.close()

    except Exception as e:
        logger.error(f"계좌 정보 조회 실패: {e}")


def show_market_info():
    """시세 조회"""
    logger = setup_logger("main")

    stock_code = input("\n종목코드를 입력하세요 (예: 005930): ").strip()

    if not stock_code:
        print("종목코드를 입력해주세요.")
        return

    try:
        market = KiwoomMarket()
        market.get_access_token()

        # 현재가 조회
        price_info = market.get_current_price(stock_code)

        print(f"\n[{price_info['종목명']} ({stock_code})]")
        print(f"현재가: {price_info['현재가']:,}원")
        print(f"전일대비: {price_info['전일대비']:+,}원 ({price_info['등락률']:+.2f}%)")
        print(f"시가: {price_info['시가']:,}원")
        print(f"고가: {price_info['고가']:,}원")
        print(f"저가: {price_info['저가']:,}원")
        print(f"거래량: {price_info['거래량']:,}주")

        market.close()

    except Exception as e:
        logger.error(f"시세 조회 실패: {e}")


def main():
    """메인 함수"""
    logger = setup_logger("main")

    while True:
        show_menu()
        choice = input("\n선택: ").strip()

        if choice == "1":
            test_connection()

        elif choice == "2":
            show_account_info()

        elif choice == "3":
            show_market_info()

        elif choice == "4":
            confirm = input("\n실제로 주문을 실행하시겠습니까? (yes/no): ").strip().lower()
            if confirm == "yes":
                run_strategy()
            else:
                print("취소되었습니다.")

        elif choice == "0":
            logger.info("프로그램을 종료합니다.")
            sys.exit(0)

        else:
            print("잘못된 선택입니다.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
        sys.exit(0)
