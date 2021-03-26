from typing import Tuple, List
import random
import numpy as np
from lib.config import config
from lib.cell import Cell

class Board:
    """ Hold board state """
    
    def __init__(self):
        """Initialize board"""
        self.cells = self.create_empty_cells()
        self.setup_board()

    @property
    def shape(self) -> Tuple[int, int]:
        """Board shape: rows, columns"""
        return self.num_rows, self.num_cols
    
    @property
    def num_rows(self) -> int:
        """Number of rows on the board"""
        return config.board_size
    
    @property
    def num_cols(self) -> int:
        """Number of columns on the board"""
        return config.board_size
    
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
        return [
            [Cell() for _ in range(self.shape[1])]
            for _ in range(self.shape[0])
        ]
    
    def is_bomb(self, row: int, col: int) -> bool:
        return self.cells[row][col].is_bomb

    def is_flag(self, row: int, col: int) -> bool:
        return self.cells[row][col].is_flagged

    def is_visible(self, row: int, col: int) -> bool:
        return self.cells[row][col].is_visible
    
    def num_nearby_bombs(self, row: int, col: int) -> int:
        return self.cells[row][col].nearby_bombs
    
    def set_bomb(self, row: int, col: int) -> None:
        """Set the specified cell as as a bomb"""
        self.cells[row][col].is_bomb = True
    
    def reveal(self, row: int, col: int) -> None:
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
        while self.num_bombs < config.num_bombs:
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
        max_row = min(row + 1, self.num_rows- 1)
        min_col = max(col - 1, 0)
        max_col = min(col + 1, self.num_cols - 1)

        total = 0
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if self.is_bomb(row, col):
                    total += 1
        
        return total

    def get_states(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return arrays of bombs, flags, counts, visibility for display"""
        bombs = np.zeros(self.shape, dtype=int)
        flags = np.zeros(self.shape, dtype=int)
        counts = np.zeros(self.shape, dtype=int)
        visible = np.zeros(self.shape, dtype=int)
        
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.is_bomb(row, col):
                    bombs[row, col] = 1
                
                if self.is_flag(row, col):
                    flags[row, col] = 1
                
                counts[row, col] = self.num_nearby_bombs(row, col)

                if self.is_visible(row, col):
                    visible[row, col] = 1
        
        return bombs, flags, counts, visible

    def show(self) -> None:
        """Print the board to screen"""
        row_spacer = "\n"
        col_spacer = " "
        bomb_string = "B"
        blank_string = "_"
        flag_string = "F"

        row_views = []
        for row in range(self.num_rows):
            col_views = []
            for col in range(self.num_cols):

                # Player knows the true state
                if self.is_visible(row, col):
                    if self.is_bomb(row, col):
                        col_views.append(bomb_string)
                    
                    else:
                        col_views.append(str(self.num_nearby_bombs(row, col)))

                # Player doesn't know the true state
                else:
                    if self.is_flag(row, col):
                        col_views.append(flag_string)

                    else:
                        col_views.append(blank_string)
            
            row_views.append(col_spacer.join(col_views))
        view = row_spacer.join(row_views)

        print(view)
            


