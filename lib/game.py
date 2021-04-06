from enum import Enum, auto
from typing import Union
from dataclasses import dataclass

from lib.config import config
from lib.board import Board


class UnknownMoveTypeError(TypeError):
    """Unknown move type"""

    pass


class UnknownGameStatusError(ValueError):
    """Unknown game status"""

    pass

class InvalidInputError(ValueError):
    """Invalid user input"""
    pass


@dataclass
class Location:
    """Hold board location"""

    row: int
    col: int


class MoveType(Enum):
    """Options for type of game moves"""

    TOGGLE_FLAG = "flag"
    REVEAL = "click"


@dataclass
class Move:
    """Hold user movement"""

    type_: MoveType
    location: Location


class Status(Enum):
    """Status of game"""

    IN_PROGRESS = auto()
    WIN = auto()
    LOSS = auto()


class Game:
    def __init__(self):
        """Setup new game"""
        self.board = Board()
        self.status = Status.IN_PROGRESS

    def play(self) -> None:
        """Play the game"""

        while self.status is Status.IN_PROGRESS:
            self.board.show()
            move = self.get_next_move()
            self.apply_move(move)

        self.board.show()
        message = self.get_game_status_message()
        print(message)

    def get_next_move(self) -> Move:
        """Get next move from user"""
        error_message = "waiting for input."
        while error_message:

            # Get user input
            error_message = ""
            message = input(
                "Enter move (flag or click) and location (row, col) "\
                "e.g. \"click 2 3\"\n"\
                ">>> "
            )
            
            # Split into 3 parts
            parts = message.split()
            if len(parts) != 3:
                error_message += "Expected 3 parts\n"
                print(error_message)
                continue
            move_str, row_str, col_str = parts

            # Get move type
            try: 
                move_type = MoveType(move_str)
            except ValueError as err:
                error_message += \
                    f"Invalid move type, should be: "\
                    f"{[t.value for t in MoveType]}\n"

            # get row and col
            try:
                row = int(row_str)
                col = int(col_str)
            except ValueError as err:
                error_message += \
                    f"Row and col must be integers.\n"
                print(error_message)
                continue

            # make sure row and col are in range
            if not (0 <= row < self.board.num_rows):
                error_message += \
                    f"Row is out of range 0-{self.board.num_rows-1}\n"
            if not (0 <= col < self.board.num_cols):
                error_message += \
                    f"Col is out of range 0,{self.board.num_cols-1}\n"
            if error_message:
                print(error_message)

        # Construct move
        return Move(type_=move_type, location=Location(row=row, col=col))

    def apply_move(self, move: Move) -> None:
        """Make the given move"""
        loc = move.location.row, move.location.col

        if move.type_ is MoveType.TOGGLE_FLAG:
            self.board.toggle_flag(*loc)

        elif move.type_ is MoveType.REVEAL:
            self.board.reveal(*loc)

            # If player revealed a bomb, the game is lost
            if self.board.is_bomb(*loc):
                self.status = Status.LOSS

            # If all but the bombs are revealed, the game won
            if self.board.all_visible_except_bombs:
                self.status = Status.WIN

        else:
            raise UnknownMoveTypeError(f"Unknown move type: {move}")

    def get_game_status_message(self):
        """Generate a message about game status"""
        if self.status is Status.IN_PROGRESS:
            return "Game is in progress"

        if self.status is Status.LOSS:
            return "Game over - You lost :("

        if self.status is Status.WIN:
            return "Game over - You won! :)"

        # Unknown status
        raise UnknownGameStatusError(f"Unknown game status: {self.status}")
