from lib.words import extract_words, group_lines
from lib.stamp import to_stamp, to_tag
from lib.revision import to_revision 
import os

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])

def to_filename(stamp, rev):
    [project, board, _, subject, _] = stamp
    tag = to_tag(stamp)
    subject = subject[:6]

    return f'SH_{tag}_{project}_{subject}_PR{board}_{rev}.pdf'

def proccess_file(file_name):
    words = extract_words(file_name)
    lines = group_lines(words)

    rev = to_revision(lines)
    stamp = to_stamp(lines)

    base_name = to_filename(stamp, rev)
    directory = os.path.dirname(file_name)
    new_file_name = os.path.join(directory, base_name)
    try:
        os.rename(file_name, new_file_name)
        logging.info(f'File successfully renamed from {file_name} to {new_file_name}')

    except OSError as e:
        logging.error(f'Error renaming file: {e}')

def process_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            if not filename.startswith('SH_') and filename.lower().endswith('.pdf'):
                file_path = os.path.join(folder_path, filename)
                logging.info(f'Processing file: {file_path}')
                proccess_file(file_path)
    except Exception as e:
        logging.error(f'Error processing folder: {e}')

process_folder('/Users/vilelamarcos/tmp/')
