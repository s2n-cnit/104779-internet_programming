import logging
import sys

from loguru import logger

logging.getLogger("passlib").setLevel(logging.ERROR)

SEP = ", "


logger_fmt = (
    "<cyan>{time:YYYY-MM-DD HH:mm:ss.SSS}</cyan> | "
    "<level>{level: <10}</level> | "
    "<level>{message}</level>"
)
config = {
    "handlers": [
        {"sink": sys.stderr, "format": logger_fmt},
    ],
}
logger.configure(**config)
