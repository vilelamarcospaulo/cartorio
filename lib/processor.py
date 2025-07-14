from lib.words import extract_words, group_lines
from lib.stamp import Stamp, to_stamp
from lib.revision import to_revision 

import logging
import os

def to_filename(stamp: Stamp, rev):
    tag = stamp.to_tag() 

    pre_hyphen = stamp.subject.split('-')[0].strip()
    subject_words = pre_hyphen.split()
    truncated_subject = '_'.join(word[:5] for word in subject_words)

    return f'SH_{tag}_{stamp.project}_{truncated_subject}_PR{stamp.drawing}_{rev}.pdf'

def proccess_file(file_path):
    if not needs_processing(file_path):
        logging.debug(f'ignored file {file_path}')
        return

    words = extract_words(file_path)
    lines = group_lines(words)

    rev = to_revision(lines)
    stamp = to_stamp(lines)

    if not stamp:
        logging.error('failed to load stamp')
        return

    base_name = to_filename(stamp, rev)
    directory = os.path.dirname(file_path)
    new_file_name = os.path.join(directory, base_name)

    if os.path.exists(new_file_name):
        logging.error(f'{new_file_name} already exists')
    else:
        try:
            os.rename(file_path, new_file_name)
            logging.info(f'File successfully renamed from {file_path} to {new_file_name}')
        except OSError as e:
            logging.error(f'Error renaming file: {e}')

def process_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        logging.info(f'Found {len(files)} items in {folder_path}')
        
        # Separate files and directories
        items = [(f, os.path.join(folder_path, f)) for f in files]

        dirs = [path for _, path in items if os.path.isdir(path)]
        files = [path for _, path in items if os.path.isfile(path)]
        
        files_to_process = filter(needs_processing, files)
        
        # Convert to list to get length for logging
        files_to_process = list(files_to_process)
        logging.info(f'Reduced to {len(files_to_process)} unprocessed .PDF files')
        
        # Process each file
        for filename in files_to_process:
            file_path = os.path.join(folder_path, filename)
            logging.info(f'Processing file: {file_path}')
            proccess_file(file_path)

        if dirs:
            logging.info(f'Found {len(dirs)} subfolders')
            # Process subfolders recursively
            for dir_path in dirs:
                logging.info(f'Processing subfolder: {dir_path}')
                process_folder(dir_path)

    except Exception as e:
        logging.error(f'Error processing folder {folder_path}: {e}')

def needs_processing(file_path):
    filename = os.path.basename(file_path)
    return (not filename.startswith('SH_')) and filename.lower().endswith('.pdf')

