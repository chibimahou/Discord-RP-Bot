import os
import logging
import asyncio
import datetime

class DiscordBotLogger:
    def __init__(self):
        # Create a 'logs' directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Get the current date in 'YYYY-MM-DD' format
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Create a logger instance for all other logs (bot-logs) and set its level to DEBUG
        self.bot_logger = logging.getLogger('bot_logger')
        self.bot_logger.setLevel(logging.DEBUG)
        
        # Create a handler for DEBUG log level and attach it to the logger
        bot_handler = logging.FileHandler(f'logs/{current_date}_bot_logs.log')
        bot_handler.setLevel(logging.DEBUG)
        bot_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.bot_logger.addHandler(bot_handler)

        # Create a logger instance for INFO logs (user-logs) and set its level to INFO
        self.user_logger = logging.getLogger('user_logger')
        self.user_logger.setLevel(logging.INFO)
        
        # Create a handler for INFO log level and attach it to the logger
        user_handler = logging.FileHandler(f'logs/{current_date}_user_logs.log')
        user_handler.setLevel(logging.INFO)
        user_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.user_logger.addHandler(user_handler)

    def log_user_info(self, message):
        self.user_logger.info(message)

    def log_bot_error(self, message):
        self.bot_logger.error(message)

    def log_bot_warning(self, message):
        self.bot_logger.warning(message)

    def log_bot_debug(self, message):
        self.bot_logger.debug(message)