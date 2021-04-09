from dataclasses import dataclass

DEFAULT_BOARD_SIZE = 10
DEFAULT_NUM_BOMBS = 5

@dataclass
class Configuration:

    board_size: int = DEFAULT_BOARD_SIZE
    num_bombs: int = DEFAULT_NUM_BOMBS
    show_outer_numbers: bool = False

    row_spacer = "\n"
    col_spacer = " "
    bomb_string = "B"
    blank_string = "."
    zero_string = "_"
    flag_string = "F"


default_config = Configuration()
