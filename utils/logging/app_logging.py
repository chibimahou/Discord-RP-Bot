import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def configure_logging():
    env = os.getenv('APP_ENV', 'local').lower()

    # Set the logging level based on the environment
    if env == 'local' or env == 'development':
        level = logging.DEBUG
    elif env == 'testing':
        level = logging.INFO
    else:  # default to production
        level = logging.WARNING

    logger = logging.getLogger()
    if logger.hasHandlers():
        # Remove all handlers associated with the root logger
        logger.handlers = []

    logger.setLevel(level)

    # Formatter with timestamp, logger name, log level, and message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # File handler that rotates logs daily
    # Getting the current date to append to the logfile name
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f'cardinal_logs_{current_date}.log'
    
    file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7)
    console_handler = logging.StreamHandler()
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    

configure_logging()
