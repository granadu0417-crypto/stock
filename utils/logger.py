"""로깅 유틸리티"""
import logging
import colorlog
from config import Config


def setup_logger(name: str = __name__) -> logging.Logger:
    """컬러 로거 설정

    Args:
        name: 로거 이름

    Returns:
        설정된 로거 객체
    """
    logger = logging.getLogger(name)

    # 이미 핸들러가 있으면 재설정하지 않음
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    # 컬러 포맷터 설정
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # 콘솔 핸들러 추가
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 파일 핸들러 추가 (선택사항)
    try:
        file_handler = logging.FileHandler('trading.log', encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"파일 핸들러 생성 실패: {e}")

    return logger
