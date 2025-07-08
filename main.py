from lib.processor import process_folder

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])

process_folder('/Users/vilelamarcos/tmp/')
