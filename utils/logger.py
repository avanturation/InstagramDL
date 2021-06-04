import logging
import sys

import colorlog

FORMATTER = colorlog.ColoredFormatter(
    "%(bold)s%(log_color)s%(levelname)s%(reset)s [%(asctime)s] [%(name)s:%(bold)s%(module)s%(reset)s] %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
    style="%",
)


class Logger:
    @staticmethod
    def generate(name: str) -> logging.Logger:
        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            stdout = logging.StreamHandler(sys.stdout)
            stdout.setFormatter(FORMATTER)
            logger.addHandler(stdout)

        return logger
