# import os
import sys
import logging
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler
# from logging.handlers import RotatingFileHandler
# from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-10s%(reset)s%(log_color)s%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

file_handler = RotatingFileHandler("app.log", maxBytes=1, backupCount=5)

stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# # config main logger
# logger = logging.getLogger("app_logger")
# logger.setLevel(logging.DEBUG)
# # log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.log")
# # log_file = os.environ.get("LOG_PATH", log_filename)
# # print(log_file)
# # Config logfile handler (log details)
# file_handler = RotatingFileHandler(
#     "app.log", maxBytes=2 * 1024 * 1024, backupCount=5
# )
# file_handler.setLevel(logging.DEBUG)  # Logs detalhados
# file_formatter = logging.Formatter(
#     "%(asctime)s - %(levelname)s - %(message)s"
# )
# file_handler.setFormatter(file_formatter)

# # Config console handler (log errors and criticals)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.ERROR)
# console_formatter = logging.Formatter(
#     "%(asctime)s - %(levelname)s - %(message)s"
# )
# console_handler.setFormatter(console_formatter)

# # Add handlers to logger instance
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# file_handler.
