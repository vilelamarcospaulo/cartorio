import logging

from dataclasses import dataclass
from typing import List
from lib.canva import Canvas, line

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

def to_stamp(canva: Canvas):
    """
    Extract stamp information from document lines starting with 'PROJETO PRANCHA'.
    """
    stamp_line= canva.find_line_by_text('PROJETO PRANCHA')
    if not stamp_line:
        logging.error('Not possible to found projeto-prancha')
        return

    stamp_header = stamp_line[1].find_word('PROJETO') 
    assert stamp_header is not None

    stamp_canva = canva.get_region(x0=stamp_header.x0,
                                   y0=stamp_header.y0)
    
    if len(stamp_canva.lines) != 8:
        logging.error('invalid stamp pattern', stamp_canva.lines)
        return

    return _coerce_stamp(stamp_canva.lines)

def _coerce_stamp(lines: List[line.Line]) -> Stamp:
    line_1 = lines[1].text.split(' ')

    drawing = line_1.pop()
    project = ' '.join(line_1)
        
    return Stamp(project, drawing, 
          lines[3].text,
          lines[5].text,
          lines[7].text)

