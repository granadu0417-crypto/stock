"""키움증권 API 설정 GUI"""
import tkinter as tk
from tkinter import ttk, messagebox
import os


class ConfigGUI:
    """설정 GUI 클래스"""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("키움증권 API 설정")
        self.window.geometry("500x400")
        self.window.resizable(False, False)

        # 환경변수 파일 경로
        self.env_path = os.path.join(os.path.dirname(__file__), ".env")

        # 기존 설정 로드
        self.load_existing_config()

        # UI 생성
        self.create_widgets()

    def load_existing_config(self):
        """기존 .env 파일에서 설정 로드"""
        self.config = {
            "KIWOOM_APP_KEY": "",
            "KIWOOM_APP_SECRET": "",
            "KIWOOM_ACCOUNT_NUMBER": "",
            "KIWOOM_ENVIRONMENT": "mock",
            "LOG_LEVEL": "INFO",
        }

        if os.path.exists(self.env_path):
            try:
                with open(self.env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            if key in self.config:
                                self.config[key] = value
            except Exception as e:
                print(f"설정 로드 실패: {e}")

    def create_widgets(self):
        """UI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 제목
        title = ttk.Label(
            main_frame,
            text="🔑 키움증권 REST API 설정",
            font=("Arial", 16, "bold"),
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # App Key
        ttk.Label(main_frame, text="App Key:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.app_key_entry = ttk.Entry(main_frame, width=40)
        self.app_key_entry.grid(row=1, column=1, pady=5)
        self.app_key_entry.insert(0, self.config["KIWOOM_APP_KEY"])

        # App Secret
        ttk.Label(main_frame, text="App Secret:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.app_secret_entry = ttk.Entry(main_frame, width=40, show="*")
        self.app_secret_entry.grid(row=2, column=1, pady=5)
        self.app_secret_entry.insert(0, self.config["KIWOOM_APP_SECRET"])

        # 계좌번호
        ttk.Label(main_frame, text="계좌번호:", font=("Arial", 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.account_entry = ttk.Entry(main_frame, width=40)
        self.account_entry.grid(row=3, column=1, pady=5)
        self.account_entry.insert(0, self.config["KIWOOM_ACCOUNT_NUMBER"])

        # 환경 선택
        ttk.Label(main_frame, text="거래 환경:", font=("Arial", 10)).grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.env_var = tk.StringVar(value=self.config["KIWOOM_ENVIRONMENT"])
        env_frame = ttk.Frame(main_frame)
        env_frame.grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Radiobutton(
            env_frame, text="모의투자", variable=self.env_var, value="mock"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            env_frame, text="실거래 ⚠️", variable=self.env_var, value="real"
        ).pack(side=tk.LEFT, padx=5)

        # 로그 레벨
        ttk.Label(main_frame, text="로그 레벨:", font=("Arial", 10)).grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        self.log_level_var = tk.StringVar(value=self.config["LOG_LEVEL"])
        log_combo = ttk.Combobox(
            main_frame,
            textvariable=self.log_level_var,
            values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            state="readonly",
            width=37,
        )
        log_combo.grid(row=5, column=1, pady=5)

        # 안내 메시지
        info_frame = ttk.LabelFrame(main_frame, text="📌 안내", padding="10")
        info_frame.grid(row=6, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))

        info_text = (
            "• 키움증권 홈페이지에서 REST API 키를 발급받으세요\n"
            "• 처음에는 반드시 '모의투자'로 테스트하세요\n"
            "• 실거래는 충분한 테스트 후 사용하세요"
        )
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack()

        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        # 저장 버튼
        save_btn = ttk.Button(
            button_frame,
            text="💾 설정 저장",
            command=self.save_config,
            width=15,
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        # 테스트 버튼
        test_btn = ttk.Button(
            button_frame,
            text="🔌 연결 테스트",
            command=self.test_connection,
            width=15,
        )
        test_btn.pack(side=tk.LEFT, padx=5)

        # 닫기 버튼
        close_btn = ttk.Button(
            button_frame, text="❌ 닫기", command=self.window.quit, width=15
        )
        close_btn.pack(side=tk.LEFT, padx=5)

    def save_config(self):
        """설정 저장"""
        app_key = self.app_key_entry.get().strip()
        app_secret = self.app_secret_entry.get().strip()
        account = self.account_entry.get().strip()
        environment = self.env_var.get()
        log_level = self.log_level_var.get()

        # 입력값 검증
        if not app_key:
            messagebox.showerror("오류", "App Key를 입력해주세요.")
            return
        if not app_secret:
            messagebox.showerror("오류", "App Secret을 입력해주세요.")
            return
        if not account:
            messagebox.showerror("오류", "계좌번호를 입력해주세요.")
            return

        # 실거래 경고
        if environment == "real":
            confirm = messagebox.askyesno(
                "⚠️ 경고",
                "실거래 환경으로 설정하시겠습니까?\n\n"
                "실제 계좌에서 거래가 실행됩니다!\n"
                "충분한 테스트 후 사용하세요.",
                icon="warning",
            )
            if not confirm:
                return

        # .env 파일 생성
        try:
            with open(self.env_path, "w", encoding="utf-8") as f:
                f.write("# 키움증권 REST API 설정\n")
                f.write(f"KIWOOM_APP_KEY={app_key}\n")
                f.write(f"KIWOOM_APP_SECRET={app_secret}\n")
                f.write(f"KIWOOM_ACCOUNT_NUMBER={account}\n")
                f.write(f"\n# API 환경 설정 (real: 실거래, mock: 모의투자)\n")
                f.write(f"KIWOOM_ENVIRONMENT={environment}\n")
                f.write(f"\n# 로깅 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)\n")
                f.write(f"LOG_LEVEL={log_level}\n")

            messagebox.showinfo(
                "성공",
                f"설정이 저장되었습니다!\n\n환경: {'모의투자' if environment == 'mock' else '실거래'}",
            )

        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 실패:\n{e}")

    def test_connection(self):
        """API 연결 테스트"""
        # 먼저 설정 저장
        self.save_config()

        try:
            # Config 다시 로드
            from importlib import reload
            import config.config as config_module

            reload(config_module)
            from config import Config
            from kiwoom.account import KiwoomAccount

            # 연결 테스트
            account = KiwoomAccount()
            account.get_access_token()

            # 계좌 정보 조회
            balance = account.get_balance()
            account.close()

            messagebox.showinfo(
                "✅ 연결 성공",
                f"API 연결에 성공했습니다!\n\n"
                f"예수금: {balance['예수금']:,}원\n"
                f"환경: {Config.KIWOOM_ENVIRONMENT}",
            )

        except Exception as e:
            messagebox.showerror("❌ 연결 실패", f"API 연결에 실패했습니다:\n\n{e}")

    def run(self):
        """GUI 실행"""
        self.window.mainloop()


if __name__ == "__main__":
    app = ConfigGUI()
    app.run()
