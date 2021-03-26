from dataclasses import dataclass


@dataclass
class Cell:
    is_bomb: bool = False
    is_visible: bool = True
    is_flagged: bool = False
    nearby_bombs: int = 0
