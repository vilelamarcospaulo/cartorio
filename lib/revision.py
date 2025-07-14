from lib.canva import Canvas
import logging
import re

def to_revision(canva: Canvas):
    """
    Extract the highest revision number from a document's revision table.
    """

    table_end_line = canva.find_line_by_text('REVISÃO DATA DESCRIÇÃO AUTORA')
    if not table_end_line:
        logging.error('Not possible to found revision-table')
        return

    rev_header = table_end_line[1].find_word('REVISÃO') 
    assert rev_header is not None

    legend_line = canva.find_line_by_text('LEGENDA')
    if not legend_line:
        logging.error('Not possible to found revision-table')
        return

    legend_header = legend_line[1].find_word('LEGENDA') 
    assert legend_header is not None

    table_canvas = canva.get_region(x0=legend_header.x0, 
                                    x1=rev_header.x1)
    # Filter lines where first word matches R followed by two digits
    valid_lines = [
        line for line in table_canvas.lines 
        if re.match(r'^R\d+$', line.words[0].text)
    ]

    if not valid_lines:
        logging.error('No valid revision lines found')
        return ''
    
    # Each line[0] is (x0, y0, x1, y1, word, block_no, line_no, word_no)
    uppermost_revision = min(valid_lines, key=lambda line: line.words[0].y0)
    result = uppermost_revision.text 
    
    return result

