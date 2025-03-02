import logging
from colorama import Fore, Style
from src.data.logs import MsgLog

# handle logger
logger = logging.getLogger("pythonLog")
LOG_COLOR = {
    logging.DEBUG: Fore.WHITE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLOR.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"


def record_msg_log(func):
    def wrapper(*args):
        msg, *_ = args

        if any(item in str(msg).lower() for item in ("step", "steps", "verify")):
            MsgLog.step_logs.append(msg)

        func(msg)

    return wrapper


def setup_logging():

    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = ColoredFormatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    _logger = logger.info

    @record_msg_log
    def log_with_record(*args):
        _logger(*args)

    logger.info = log_with_record
