"""키움증권 자동매매 GUI 메인 프로그램"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import os
from datetime import datetime


class TradingGUI:
    """자동매매 GUI 메인 클래스"""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🤖 키움증권 자동매매 프로그램")
        self.window.geometry("900x700")

        # 스타일 설정
        self.setup_styles()

        # UI 생성
        self.create_widgets()

        # API 클라이언트 초기화 (나중에)
        self.market = None
        self.account = None
        self.order = None
        self.is_connected = False

    def setup_styles(self):
        """스타일 설정"""
        style = ttk.Style()
        style.theme_use("clam")

    def create_widgets(self):
        """UI 위젯 생성"""
        # 상단 메뉴바
        self.create_menu()

        # 메인 프레임
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 좌측 패널 (계좌 정보)
        left_frame = ttk.LabelFrame(main_frame, text="📊 계좌 정보", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.create_account_panel(left_frame)

        # 우측 패널 (제어 및 로그)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 제어 패널
        control_frame = ttk.LabelFrame(right_frame, text="🎮 제어 패널", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        self.create_control_panel(control_frame)

        # 시세 조회 패널
        quote_frame = ttk.LabelFrame(right_frame, text="📈 시세 조회", padding="10")
        quote_frame.pack(fill=tk.X, pady=(0, 10))
        self.create_quote_panel(quote_frame)

        # 로그 패널
        log_frame = ttk.LabelFrame(right_frame, text="📝 로그", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.create_log_panel(log_frame)

        # 하단 상태바
        self.create_statusbar()

    def create_menu(self):
        """메뉴바 생성"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="설정", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.window.quit)

        # 도구 메뉴
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도구", menu=tools_menu)
        tools_menu.add_command(label="연결 테스트", command=self.test_connection)
        tools_menu.add_command(label="계좌 새로고침", command=self.refresh_account)

        # 도움말 메뉴
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도움말", menu=help_menu)
        help_menu.add_command(label="사용법", command=self.show_help)
        help_menu.add_command(label="정보", command=self.show_about)

    def create_account_panel(self, parent):
        """계좌 정보 패널"""
        # 잔고 정보
        balance_frame = ttk.Frame(parent)
        balance_frame.pack(fill=tk.X, pady=(0, 10))

        labels = ["예수금", "총평가금액", "총손익", "수익률"]
        self.balance_labels = {}

        for i, label in enumerate(labels):
            ttk.Label(balance_frame, text=f"{label}:", font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky=tk.W, pady=3
            )
            value_label = ttk.Label(balance_frame, text="0원", font=("Arial", 10))
            value_label.grid(row=i, column=1, sticky=tk.E, pady=3)
            self.balance_labels[label] = value_label

        # 보유 종목 테이블
        ttk.Label(parent, text="보유 종목:", font=("Arial", 10, "bold")).pack(
            anchor=tk.W, pady=(10, 5)
        )

        columns = ("종목명", "수량", "현재가", "손익", "수익률")
        self.stocks_tree = ttk.Treeview(
            parent, columns=columns, show="headings", height=10
        )

        for col in columns:
            self.stocks_tree.heading(col, text=col)
            if col == "종목명":
                self.stocks_tree.column(col, width=120)
            else:
                self.stocks_tree.column(col, width=80, anchor=tk.E)

        self.stocks_tree.pack(fill=tk.BOTH, expand=True)

        # 스크롤바
        scrollbar = ttk.Scrollbar(
            parent, orient=tk.VERTICAL, command=self.stocks_tree.yview
        )
        self.stocks_tree.configure(yscroll=scrollbar.set)

    def create_control_panel(self, parent):
        """제어 패널"""
        # 연결 상태
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(status_frame, text="연결 상태:", font=("Arial", 10)).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        self.status_label = ttk.Label(
            status_frame, text="❌ 미연결", font=("Arial", 10, "bold"), foreground="red"
        )
        self.status_label.pack(side=tk.LEFT)

        # 버튼 프레임
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="🔌 연결", command=self.connect_api, width=12).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(
            btn_frame, text="🔄 새로고침", command=self.refresh_account, width=12
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame, text="⚙️ 설정", command=self.open_settings, width=12
        ).pack(side=tk.LEFT, padx=2)

    def create_quote_panel(self, parent):
        """시세 조회 패널"""
        # 종목코드 입력
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="종목코드:").pack(side=tk.LEFT, padx=(0, 5))
        self.stock_code_entry = ttk.Entry(input_frame, width=10)
        self.stock_code_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(input_frame, text="조회", command=self.get_quote).pack(side=tk.LEFT)

        # 시세 정보
        self.quote_text = tk.Text(parent, height=6, font=("Courier", 9))
        self.quote_text.pack(fill=tk.X)
        self.quote_text.insert("1.0", "종목코드를 입력하고 조회 버튼을 클릭하세요.")
        self.quote_text.config(state=tk.DISABLED)

    def create_log_panel(self, parent):
        """로그 패널"""
        self.log_text = scrolledtext.ScrolledText(
            parent, height=15, font=("Courier", 9), wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 로그 태그 색상
        self.log_text.tag_config("INFO", foreground="green")
        self.log_text.tag_config("WARNING", foreground="orange")
        self.log_text.tag_config("ERROR", foreground="red")

        self.log("프로그램이 시작되었습니다.", "INFO")
        self.log("설정 메뉴에서 API 키를 입력하세요.", "INFO")

    def create_statusbar(self):
        """하단 상태바"""
        self.statusbar = ttk.Label(
            self.window,
            text="준비",
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2),
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def log(self, message, level="INFO"):
        """로그 메시지 출력"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}\n"

        self.log_text.insert(tk.END, log_msg, level)
        self.log_text.see(tk.END)

    def update_status(self, message):
        """상태바 업데이트"""
        self.statusbar.config(text=message)

    def open_settings(self):
        """설정 창 열기"""
        self.log("설정 창을 엽니다.", "INFO")
        os.system(f"{sys.executable} config_gui.py")

    def test_connection(self):
        """연결 테스트"""
        self.connect_api()

    def connect_api(self):
        """API 연결"""
        self.log("API에 연결을 시도합니다...", "INFO")
        self.update_status("연결 중...")

        def connect_thread():
            try:
                from config import Config
                from kiwoom.account import KiwoomAccount
                from kiwoom.market import KiwoomMarket
                from kiwoom.order import KiwoomOrder

                # 설정 검증
                Config.validate()

                # API 클라이언트 초기화
                self.account = KiwoomAccount()
                self.account.get_access_token()

                self.market = KiwoomMarket()
                self.market.access_token = self.account.access_token

                self.order = KiwoomOrder()
                self.order.access_token = self.account.access_token

                self.is_connected = True

                # UI 업데이트 (메인 스레드에서)
                self.window.after(
                    0,
                    lambda: self.status_label.config(
                        text="✅ 연결됨", foreground="green"
                    ),
                )
                self.window.after(0, lambda: self.log("API 연결 성공!", "INFO"))
                self.window.after(0, lambda: self.update_status("연결됨"))
                self.window.after(0, self.refresh_account)

            except Exception as e:
                self.window.after(0, lambda: self.log(f"연결 실패: {e}", "ERROR"))
                self.window.after(
                    0, lambda: messagebox.showerror("연결 실패", f"API 연결 실패:\n{e}")
                )
                self.window.after(0, lambda: self.update_status("연결 실패"))

        threading.Thread(target=connect_thread, daemon=True).start()

    def refresh_account(self):
        """계좌 정보 새로고침"""
        if not self.is_connected:
            messagebox.showwarning("경고", "먼저 API에 연결하세요.")
            return

        self.log("계좌 정보를 조회합니다...", "INFO")
        self.update_status("계좌 조회 중...")

        def refresh_thread():
            try:
                # 잔고 조회
                balance = self.account.get_balance()

                # 잔고 라벨 업데이트
                self.window.after(
                    0,
                    lambda: self.balance_labels["예수금"].config(
                        text=f"{balance['예수금']:,}원"
                    ),
                )
                self.window.after(
                    0,
                    lambda: self.balance_labels["총평가금액"].config(
                        text=f"{balance['총평가금액']:,}원"
                    ),
                )
                self.window.after(
                    0,
                    lambda: self.balance_labels["총손익"].config(
                        text=f"{balance['총손익']:,}원",
                        foreground="red" if balance["총손익"] < 0 else "green",
                    ),
                )
                self.window.after(
                    0,
                    lambda: self.balance_labels["수익률"].config(
                        text=f"{balance['수익률']:+.2f}%",
                        foreground="red" if balance["수익률"] < 0 else "green",
                    ),
                )

                # 보유 주식 조회
                stocks = self.account.get_stock_balance()

                # 테이블 초기화
                self.window.after(
                    0, lambda: self.stocks_tree.delete(*self.stocks_tree.get_children())
                )

                # 테이블 업데이트
                for stock in stocks:
                    profit_color = "red" if stock["평가손익"] < 0 else "green"
                    self.window.after(
                        0,
                        lambda s=stock: self.stocks_tree.insert(
                            "",
                            tk.END,
                            values=(
                                s["종목명"],
                                f"{s['보유수량']}주",
                                f"{s['현재가']:,}원",
                                f"{s['평가손익']:,}원",
                                f"{s['수익률']:+.2f}%",
                            ),
                        ),
                    )

                self.window.after(0, lambda: self.log("계좌 정보 조회 완료", "INFO"))
                self.window.after(0, lambda: self.update_status("준비"))

            except Exception as e:
                self.window.after(0, lambda: self.log(f"조회 실패: {e}", "ERROR"))
                self.window.after(0, lambda: self.update_status("조회 실패"))

        threading.Thread(target=refresh_thread, daemon=True).start()

    def get_quote(self):
        """시세 조회"""
        if not self.is_connected:
            messagebox.showwarning("경고", "먼저 API에 연결하세요.")
            return

        stock_code = self.stock_code_entry.get().strip()
        if not stock_code:
            messagebox.showwarning("경고", "종목코드를 입력하세요.")
            return

        self.log(f"{stock_code} 시세 조회 중...", "INFO")

        def quote_thread():
            try:
                price_info = self.market.get_current_price(stock_code)

                quote_text = (
                    f"종목명: {price_info['종목명']} ({stock_code})\n"
                    f"현재가: {price_info['현재가']:,}원\n"
                    f"전일대비: {price_info['전일대비']:+,}원 ({price_info['등락률']:+.2f}%)\n"
                    f"시가: {price_info['시가']:,}원 | 고가: {price_info['고가']:,}원 | 저가: {price_info['저가']:,}원\n"
                    f"거래량: {price_info['거래량']:,}주"
                )

                self.window.after(
                    0,
                    lambda: self.quote_text.config(state=tk.NORMAL),
                )
                self.window.after(
                    0,
                    lambda: self.quote_text.delete("1.0", tk.END),
                )
                self.window.after(
                    0,
                    lambda: self.quote_text.insert("1.0", quote_text),
                )
                self.window.after(
                    0,
                    lambda: self.quote_text.config(state=tk.DISABLED),
                )

                self.window.after(0, lambda: self.log("시세 조회 완료", "INFO"))

            except Exception as e:
                self.window.after(0, lambda: self.log(f"시세 조회 실패: {e}", "ERROR"))

        threading.Thread(target=quote_thread, daemon=True).start()

    def show_help(self):
        """사용법 표시"""
        help_text = """
        🤖 키움증권 자동매매 프로그램 사용법

        1. 설정 메뉴에서 API 키를 입력하세요
        2. '연결' 버튼을 클릭하여 API에 연결하세요
        3. 계좌 정보와 보유 종목을 확인하세요
        4. 시세 조회 패널에서 종목 시세를 확인하세요

        ⚠️ 주의사항:
        - 처음에는 반드시 모의투자로 테스트하세요
        - 실거래는 충분한 테스트 후 사용하세요
        - 자동매매는 손실 위험이 있습니다
        """
        messagebox.showinfo("사용법", help_text)

    def show_about(self):
        """정보 표시"""
        about_text = """
        키움증권 REST API 자동매매 프로그램

        버전: 1.0.0

        키움증권의 REST API를 활용한
        주식 자동매매 시스템입니다.
        """
        messagebox.showinfo("정보", about_text)

    def run(self):
        """GUI 실행"""
        self.window.mainloop()


if __name__ == "__main__":
    app = TradingGUI()
    app.run()
