from lib.words import extract_words, group_lines
from lib.stamp import to_stamp, to_tag
from lib.revision import to_revision 

import logging
import os

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
    if os.path.exists(new_file_name):
        logging.error(f'{new_file_name} already exists')
    else:
        try:
            os.rename(file_name, new_file_name)
            logging.info(f'File successfully renamed from {file_name} to {new_file_name}')
        except OSError as e:
            logging.error(f'Error renaming file: {e}')

def process_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        logging.info(f'Found {len(files)} items in {folder_path}')
        
        # Separate files and directories
        items = [(f, os.path.join(folder_path, f)) for f in files]
        dirs = [path for _, path in items if os.path.isdir(path)]
        files = [f for f, _ in items if os.path.isfile(os.path.join(folder_path, f))]
        
        def is_pdf(filename):
            return filename.lower().endswith('.pdf')
        
        def needs_processing(filename):
            return not filename.startswith('SH_')
        
        # Filter PDF files that need processing
        pdf_files = filter(is_pdf, files)
        files_to_process = filter(needs_processing, pdf_files)
        
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
