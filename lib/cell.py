from dataclasses import dataclass


@dataclass
class Cell:
    is_bomb: bool = False
    is_visible: bool = False
    is_flagged: bool = False
    nearby_bombs: int = 0
