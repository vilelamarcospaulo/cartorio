from lib.processor import process_folder

import logging
import argparse
import os.path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])

def main():
    parser = argparse.ArgumentParser(description='Process a folder')
    parser.add_argument('path', help='Path to the folder to process')
    args = parser.parse_args()
    
    # Normalize path for cross-platform compatibility
    normalized_path = os.path.normpath(args.path)
    process_folder(normalized_path)

if __name__ == '__main__':
    main()
