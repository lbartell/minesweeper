from typing import Tuple, List
import random

from lib.config import default_config, Configuration
from lib.types import Cell


class Board:
    """ Hold board state """

    def __init__(self, config: Configuration = default_config):
        """Initialize board"""
        self.config = config
        self.cells = self.create_empty_cells()
        self.setup_board()

    @property
    def shape(self) -> Tuple[int, int]:
        """Board shape: rows, columns"""
        return self.num_rows, self.num_cols

    @property
    def num_rows(self) -> int:
        """Number of rows on the board"""
        return self.config.board_size

    @property
    def num_cols(self) -> int:
        """Number of columns on the board"""
        return self.config.board_size

    @property
    def num_bombs(self) -> int:
        """Return number of bombs on the board"""
        total = 0
        for row in self.cells:
            for cell in row:
                if cell.is_bomb:
                    total += 1
        return total

    def create_empty_cells(self) -> List[List[Cell]]:
        """Create an array of empty cells"""
        return [[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)]

    def is_bomb(self, row: int, col: int) -> bool:
        return self.cells[row][col].is_bomb

    def is_flag(self, row: int, col: int) -> bool:
        return self.cells[row][col].is_flagged

    def is_visible(self, row: int, col: int) -> bool:
        return self.cells[row][col].is_visible

    def num_bombs_nearby(self, row: int, col: int) -> int:
        return self.cells[row][col].nearby_bombs

    def set_bomb(self, row: int, col: int) -> None:
        """Set the specified cell as as a bomb"""
        self.cells[row][col].is_bomb = True

    def reveal(self, row: int, col: int) -> None:
        """Set the specified cell as visible, as well as all neighbors"""
        if self.is_bomb(row, col):
            self._reveal_single(row, col)
            return

        self._reveal_recursive(row, col)

    def _reveal_recursive(self, row: int, col: int) -> None:
        """Recursively reveal cells in the neighborhood"""
        for delta in range(-1, 2):
            for gamma in range(-1, 2):

                r = row + delta
                c = col + gamma

                valid_location = (0 <= r < self.num_rows) and (0 <= c < self.num_cols)

                if not valid_location:
                    continue

                if self.is_visible(r, c):
                    continue

                if self.is_bomb(r, c):
                    continue

                if self.num_bombs_nearby(r, c) == 0:
                    self._reveal_single(r, c)
                    self._reveal_recursive(r, c)
                    continue

                if self.num_bombs_nearby(r, c) > 0:
                    self._reveal_single(r, c)
                    continue

    def _reveal_single(self, row: int, col: int) -> None:
        """Set the specified cell as visible"""
        self.cells[row][col].is_visible = True

    def toggle_flag(self, row: int, col: int) -> None:
        """Toggle the flag on the specified cell"""
        current_state = self.cells[row][col].is_flagged
        self.cells[row][col].is_flagged = not current_state

    def setup_board(self) -> None:
        """Create bombs and update neighbor bomb counts"""
        self.create_bombs()
        self.update_counts()

    def create_bombs(self) -> None:
        """Create bombs on the board"""
        while self.num_bombs < self.config.num_bombs:
            row = random.randrange(self.shape[0])
            col = random.randrange(self.shape[1])
            self.set_bomb(row, col)

    def update_counts(self) -> None:
        """For each cell, update the count of number of bombs nearby"""
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                num_bombs_nearby = self.count_num_bombs_nearby(row, col)
                self.cells[row][col].nearby_bombs = num_bombs_nearby

    def count_num_bombs_nearby(self, row: int, col: int) -> int:
        """Count number of bombs near the specified cell"""
        min_row = max(row - 1, 0)
        max_row = min(row + 1, self.num_rows - 1)
        min_col = max(col - 1, 0)
        max_col = min(col + 1, self.num_cols - 1)

        total = 0
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if self.is_bomb(row, col):
                    total += 1

        return total

    @property
    def all_visible_except_bombs(self) -> bool:
        """Return True if all cells are visible except bombs, False otherwise"""
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.is_bomb(row, col):
                    continue
                if not self.is_visible(row, col):
                    return False

        return True

    def show(self, show_all: bool = False) -> None:
        """Print the board to screen

        Args
            show_all: if True, ignore visibility flag and show the full board state
        """
        row_views = []
        for row in range(self.num_rows):
            col_views = []
            for col in range(self.num_cols):

                # Show the true state
                if self.is_visible(row, col) or show_all:
                    if self.is_bomb(row, col):
                        col_views.append(self.config.bomb_string)

                    else:
                        nearby_bombs = self.num_bombs_nearby(row, col)
                        if nearby_bombs > 0:
                            col_views.append(str(nearby_bombs))
                        else:
                            col_views.append(self.config.zero_string)

                # Don't show the true state
                else:
                    if self.is_flag(row, col):
                        col_views.append(self.config.flag_string)

                    else:
                        col_views.append(self.config.blank_string)

            row_views.append(self.config.col_spacer.join(col_views))
        view = self.config.row_spacer.join(row_views)

        print(view)
