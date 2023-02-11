import logging
import os

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(log_dir, log_file, level=logging.INFO):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, log_file)
    logging.basicConfig(
        filename=log_file, level=level, format=LOG_FORMAT, datefmt=DATE_FORMAT
    )


def get_logger(name):
    return logging.getLogger(name)
