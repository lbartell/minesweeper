"""
Custom data types
"""
from dataclasses import dataclass
from enum import Enum, auto


class MoveType(Enum):
    """Options for type of game moves"""

    TOGGLE_FLAG = "flag"
    REVEAL = "click"


class Status(Enum):
    """Status of a game"""

    IN_PROGRESS = auto()
    WIN = auto()
    LOSS = auto()


@dataclass
class Cell:
    """Hold state of one cell on the board"""

    is_bomb: bool = False
    is_visible: bool = False
    is_flagged: bool = False
    nearby_bombs: int = 0


@dataclass
class Location:
    """Hold location on the board"""

    row: int
    col: int


@dataclass
class Move:
    """Hold user movement"""

    type_: MoveType
    location: Location
