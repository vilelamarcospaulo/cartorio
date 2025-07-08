from lib.words import find_line_index

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
        logging.debug('Revision header not found')
        return

    legend_index = find_line_index(lines, 'LEGENDA')
    if legend_index == -1:
        logging.debug('Legend header not found')
        return

    revision_table = lines[legend_index:revision_index]
    
    # Filter lines where first word matches R followed by two digits
    valid_lines = [
        line for line in revision_table 
        if re.match(r'^R\d+$', line[0][4])
    ]
    
    if not valid_lines:
        logging.debug('No valid revision lines found')
        return ''
        
    # Each line[0] is (x0, y0, x1, y1, word, block_no, line_no, word_no)
    uppermost_revision = min(valid_lines, key=lambda line: line[0][1])
    result = uppermost_revision[0][4]
    
    return result

