
import logging
import sys
from datetime import datetime
from pathlib import Path
from config.config import LOGS_DIR, LOG_LEVEL, LOG_FORMAT


def get_logger(name):
    """
    Create and configure a logger instance

    Args:
        name (str): Logger name (typically __name__ of the calling module)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_filename = f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = LOGS_DIR / log_filename

    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Create a default logger for the framework
default_logger = get_logger("AutomationFramework")