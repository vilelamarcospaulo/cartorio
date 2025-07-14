from dataclasses import dataclass
from typing import Tuple 

@dataclass
class Word:
    """Represents a single word with its position and metadata."""
    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    block_no: int
    line_no: int
    word_no: int
    
    @classmethod
    def from_tuple(cls, word_tuple: Tuple) -> 'Word':
        return cls(*word_tuple)
    
    @property
    def center_x(self) -> float:
        return (self.x0 + self.x1) / 2
    
    @property
    def center_y(self) -> float:
        return (self.y0 + self.y1) / 2

