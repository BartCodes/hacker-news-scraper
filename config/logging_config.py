import logging
import sys

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def setup_logging():
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format=LOGGING_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )