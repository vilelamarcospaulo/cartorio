from .canva import Canvas
from .word import Word

import logging
import pymupdf

def from_pdf(path):
    try:
        doc = pymupdf.open(path)
        page = doc[0] 
        words = page.get_text('words', sort=True) 

        doc.close()

        if not words:
            logging.error(f'PDF {path} :: without any content')
            return

        logging.debug(f'PDF {path} :: extracted {len(words)} words')

        words = [Word.from_tuple(x) for x in words]
        return Canvas(words) 

    except Exception as e:
        logging.error(f'Error extracting PDF content: {e}')
        return
