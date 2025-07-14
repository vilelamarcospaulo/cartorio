from lib.processor import process_folder

import logging
import argparse
import os.path

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])

def main(path: str):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        logging.error(f'Invalid path: {path}')
        return

    logging.info(f'Processing folder: {path}')
    try:
        process_folder(path)
    except Exception as e:
        logging.exception(f'[runner] Failed to process folder {path}: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run process in some folder (recursively).')
    parser.add_argument('path', help='Path to the folder to process or observe')
    args = parser.parse_args()

    main(args.path)
