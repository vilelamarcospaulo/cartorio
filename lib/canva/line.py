from dataclasses import dataclass
from typing import List, Optional

from .word import Word

@dataclass
class Line:
    """Represents a line in the file."""
    words: List[Word]
    y_coord: float
    
    @property
    def text(self) -> str:
        return ' '.join(word.text for word in self.words)
    
    def find_word(self, search_text: str, case_sensitive: bool = False) -> Optional[Word]:
        """Find a word in this line."""
        search = search_text if case_sensitive else search_text.lower()
        for word in self.words:
            word_text = word.text if case_sensitive else word.text.lower()
            if word_text == search:
                return word
        return None
    
    def words_after_x(self, x_threshold: float) -> List[Word]:
        """Get words that start after the given x coordinate."""
        return [word for word in self.words if word.x0 >= x_threshold]
