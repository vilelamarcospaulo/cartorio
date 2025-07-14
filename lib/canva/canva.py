from typing import List, Tuple, Dict, Optional
import logging

from .word import Word
from .line import Line

import re
class Canvas:
    """Represents the entire document canvas with positioning and search capabilities."""
    
    def __init__(self, words: List[Word]):
        self.words = words
        self.lines = self._group_into_lines()

    def find_line_by_text(self, search_text: str, exact_match: bool = False) -> Optional[Tuple[int, Line]]:
        """Find a line by its text content."""
        for i, line in enumerate(self.lines):
            if exact_match:
                if line.text == search_text:
                    logging.debug(f'Found exact pattern "{search_text}" at line {i}')
                    return i, line
            else:
                if search_text in line.text:
                    logging.debug(f'Found pattern "{search_text}" in line {i}: "{line.text}"')
                    return i, line
        
        logging.debug(f'Pattern "{search_text}" not found')
        return None


    def get_region(self, *,
                   x0: float = 0,              y0: float = 0, 
                   x1: Optional[float] = None, y1: Optional[float] = None) -> 'Canvas':
        """Get a new canvas containing only words within the specified rectangular region.
        
        Args:
            x0: Left boundary (default: 0)
            y0: Top boundary (default: 0)
            x1: Right boundary (default: infinity - no right limit)
            y1: Bottom boundary (default: infinity - no bottom limit)
        """
        # Set defaults to infinity if not provided
        if x1 is None:
            x1 = float('inf')
        if y1 is None:
            y1 = float('inf')
            
        filtered_words = []
        
        for word in self.words:
            # Check if word is within the rectangular bounds
            if (word.x0 >= x0 and word.y0 >= y0 and 
                word.x1 <= x1 and word.y1 <= y1):
                filtered_words.append(word)
        
        return Canvas(filtered_words)
    

    def _group_into_lines(self, y_threshold: float = 3) -> List[Line]:
        """Group words into lines based on Y coordinates."""
        if not self.words:
            return []
        
        # Group by Y coordinate with threshold
        y_groups: Dict[float, List[Word]] = {}
        
        for word in self.words:
            # Find closest existing Y coordinate
            matching_y = None
            for existing_y in y_groups.keys():
                if abs(existing_y - word.y0) <= y_threshold:
                    matching_y = existing_y
                    break
            
            if matching_y is None:
                y_groups[word.y0] = [word]
            else:
                y_groups[matching_y].append(word)
        
        # Create Line objects and sort
        lines = []
        for y_coord, words in y_groups.items():
            words.sort(key=lambda w: w.x0)  # Sort words by X coordinate
            lines.append(Line(words, y_coord))
        
        # Sort lines by Y coordinate (top to bottom)
        lines.sort(key=lambda line: line.y_coord)
        return lines
