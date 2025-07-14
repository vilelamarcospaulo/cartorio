from lib.words import find_line_index, find_line_word

import logging
import re

def to_revision(lines):
    """
    Extract the highest revision number from a document's revision table.
    
    Args:
        lines: List of lines, where each line contains word tuples
              (x0, y0, x1, y1, word, block_no, line_no, word_no)
    
    Returns:
        str: The highest revision number found, or empty string if not found
    """

    revision_index = find_line_index(lines, 'REVISÃO DATA DESCRIÇÃO AUTORA')
    if revision_index == -1:
        logging.error('Revision header not found')
        return

    legend_index = find_line_index(lines, 'LEGENDA')
    if legend_index == -1:
        logging.error('Legend header not found')
        return

    revision_table = lines[legend_index:revision_index]

    # Get header word position
    revision_header = find_line_word(lines[revision_index], 'REVISÃO')
    if not revision_header:
        return

    header_x = revision_header[0]
    revision_table = lines[legend_index:revision_index]

    # Filter revision table to only include words after header x position
    filtered_table = []
    for line in revision_table:
        filtered_line = []
        for word in line:
            if word[0] >= header_x:
                filtered_line.append(word)

        if filtered_line:
            filtered_table.append(filtered_line)

    # Filter lines where first word matches R followed by two digits
    valid_lines = [
        line for line in filtered_table 
        if line and re.match(r'^R\d+$', line[0][4])
    ]

    if not valid_lines:
        logging.error('No valid revision lines found')
        return ''
    
    # Each line[0] is (x0, y0, x1, y1, word, block_no, line_no, word_no)
    uppermost_revision = min(valid_lines, key=lambda line: line[0][1])
    result = uppermost_revision[0][4]
    
    return result

