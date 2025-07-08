from lib.processor import process_folder

from ports.wd import WatchdogRunner

import logging
import argparse
import os.path

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])

def main(mode: str, path: str):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        logging.error(f'[{mode}] Invalid path: {path}')
        return

    if mode == 'runner':
        logging.info(f'[runner] Processing folder: {path}')
        try:
            process_folder(path)
        except Exception as e:
            logging.exception(f'[runner] Failed to process folder {path}: {e}')

    elif mode == 'watch':
        logging.info(f'[watcher] Starting watcher for: {path}')
        try:
            WatchdogRunner(path).start()
        except Exception as e:
            logging.exception(f'[watcher] Failed to start watcher on {path}: {e}')
    else:
        logging.error(f'[main] Unknown mode: {mode}. Use runner or watch.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run in watcher or runner mode to process a folder.')
    parser.add_argument('mode', choices=['runner', 'watch'], help='Execution mode: runner or watcher')
    parser.add_argument('path', help='Path to the folder to process or observe')
    args = parser.parse_args()

    main(args.mode, args.path)
