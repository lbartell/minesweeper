from dataclasses import dataclass


@dataclass
class Configuration:

    board_size: int = 10
    num_bombs: int = 5

    row_spacer = "\n"
    col_spacer = " "
    bomb_string = "B"
    blank_string = "."
    zero_string = "_"
    flag_string = "F"


default_config = Configuration()
