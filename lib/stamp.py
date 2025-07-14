import logging

from dataclasses import dataclass
from typing import Optional
from lib.words import find_line_index, find_line_word, line_to_str

@dataclass
class Stamp:
    """Represents a document stamp with key information fields."""
    project: str
    drawing: str
    stage: str
    subject: str
    details: str

    def to_tag(self) -> str:
        """Convert stamp to document tag."""
        if 'SINALIZAÇÃO' in self.project:
            return 'SCV'

        return 'ARQ'

def to_stamp(lines): 
    """
    Extract stamp information from document lines starting with 'PROJETO PRANCHA'.
    
    Args:
        lines: List of lines, where each line contains word tuples
              (x0, y0, x1, y1, word, block_no, line_no, word_no)
    
    Returns:
        list: A processed list containing 5 elements:
            [project_name, revision, text_line3, text_line5, text_line7]
        or None if 'PROJETO PRANCHA' is not found
    """
    stamp_line_index = find_line_index(lines, 'PROJETO PRANCHA')
    if stamp_line_index == -1:
        return

    stamp_header = find_line_word(lines[stamp_line_index], 'PROJETO')
    if not stamp_header:
        return

    # Get header coordinates
    header_x = stamp_header[0]
    header_y = stamp_header[1]

    # Filter lines and words that are after header position
    stamp = []
    for line in lines[stamp_line_index:]:
        filtered_line = []
        for word in line:
            if word[0] >= header_x and word[1] >= header_y:
                filtered_line.append(word)

        if filtered_line:
            stamp.append(filtered_line)

    stamp = [line_to_str(x) for x in stamp]
    if len(stamp) != 8:
        logging.error('invalid stamp pattern', stamp)
        return

    return _coerce_stamp(stamp)

def _coerce_stamp(texts) -> Stamp:
    line_1 = texts[1].split(' ')
    drawing = line_1.pop()
    project = ' '.join(line_1)
        
    return Stamp(project, drawing, 
          texts[3],
          texts[5],
          texts[7])

