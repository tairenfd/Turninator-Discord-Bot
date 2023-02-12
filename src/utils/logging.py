import logging
import os

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(log_dir: str, log_file: str, level: int = logging.INFO) -> None:
    """
    Set up the logging mechanism.

    Parameters:
        log_dir (str): The path to the log directory.
        log_file (str): The name of the log file.
        level (int, optional): The level of the logger. Defaults to logging.INFO.

    Returns:
        None

    Example:
        >>> setup_logger("logs", "my_log.log")
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, log_file)
    logging.basicConfig(
        filename=log_file, level=level, format=LOG_FORMAT, datefmt=DATE_FORMAT
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Parameters:
        name (str): The name of the logger.

    Returns:
        logger (logging.Logger): The logger instance.

    Example:
        >>> logger = get_logger("my_log")
        >>> logger.info("Some message")
    """
    return logging.getLogger(name)
