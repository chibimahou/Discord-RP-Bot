from start_bot import run
from utils.logging.app_logging import configure_logging

# Your other imports and setup code

def main():
    # Your initialization and configuration code

    # Call the run_bot() function from character_bot.py
    run()

import start_bot
# Check if this file is being run as the main module
if __name__ == '__main__':
    configure_logging()
    main()
