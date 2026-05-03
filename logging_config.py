import logging
import os
from datetime import datetime

def setup_logger(name='trading_bot'):
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    fh = logging.FileHandler(f'logs/trading_bot_{datetime.now().strftime(chr(37)+'Y'+chr(37)+'m'+chr(37)+'d')}.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
