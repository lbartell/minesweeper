from dataclasses import dataclass

@dataclass
class Configuration:
    board_size: int = 10
    num_bombs: int = 5
    

config = Configuration()
