import logging
import pymupdf

def extract_words(pdf_path):
    try:
        doc = pymupdf.open(pdf_path)
        page = doc[0] 
        words = page.get_text('words', sort=True) 

        doc.close()

        if not words:
            logging.error(f'PDF {pdf_path} :: without any content')
            return None

        logging.debug(f'PDF {pdf_path} :: extracted {len(words)} words')
        return words
        
    except Exception as e:
        logging.error(f'Error extracting PDF content: {e}')
        return None

def group_lines(words):
    """
    Group words into lines based on their Y coordinates.
    
    Args:
        words: List of word tuples from PDF extraction
        Each tuple contains (x0, y0, x1, y1, word, block_no, line_no, word_no)
    
    Returns:
        list: List of lines, where each line is a list of words on that Y coordinate
    """
    if not words:
        return []

    # Dictionary to store words grouped by their Y coordinate
    lines = {}
    
    # Small threshold for Y coordinate differences (to account for slight misalignments)
    Y_THRESHOLD = 3
    
    for word_tuple in words:
        y_coord = word_tuple[1]  # y0 coordinate
        
        # Find the closest existing y coordinate within threshold
        matching_y = None
        for existing_y in lines.keys():
            if abs(existing_y - y_coord) <= Y_THRESHOLD:
                matching_y = existing_y
                break
        
        # If no matching y coordinate found, create new line
        if matching_y is None:
            lines[y_coord] = [word_tuple]
        else:
            lines[matching_y].append(word_tuple)
    
    result = []
    for line in lines.values():
        line.sort(key=lambda x: x[0])  
        result.append(line)

    return sorted(result, 
                  key=lambda x: (x[0][1], x[0][0]))
    
   
def find_line_index(lines: list[list], search: str) -> int:
    """
    Find the index where a sequence of strings matches consecutive lines.
    
    Args:
        lines: List of lines, where each line contains word tuples
              (x0, y0, x1, y1, word, block_no, line_no, word_no)
        search_terms: List of strings to search for in sequence
    
    Returns:
        int: Starting index where the sequence was found, or -1 if not found
    """
    if not lines or not search:
        return -1
    
    for i, l in enumerate(lines):
        l_str = line_to_str(l)
        if l_str == search:
            logging.debug(f'pattern {search} :: index {i}')
            return i
    

    logging.debug(f'pattern {search} :: not found')
    return -1

def line_to_str(line):
    """
    Convert word tuples into readable text strings.
    
    Args:
        line: list of word tuples
        
    Returns:
        list: string representing a line of text
    """
    return ' '.join(word[4] for word in line)
