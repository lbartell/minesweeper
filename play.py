"""
Play a game!
"""
from argparse import ArgumentParser
import sys
from typing import List

from lib.game import Game
from lib.config import (Configuration,
                        DEFAULT_BOARD_SIZE,
                        DEFAULT_NUM_BOMBS)

def parse_args(args_list: List[str]) -> Configuration:
    """Parse arguments"""
    parser = ArgumentParser(description="Minesweeper")

    parser.add_argument(
        "--size",
        "-s",
        help=f"Board side length, e.g. input 10 for a 10x10 board. (default {DEFAULT_BOARD_SIZE})",
        type=int,
        default=DEFAULT_BOARD_SIZE,
        dest="board_size",
    )

    parser.add_argument(
        "--bombs",
        "-b",
        help=f"Number of bombs to place on the board. (default {DEFAULT_NUM_BOMBS})",
        type=int,
        default=DEFAULT_NUM_BOMBS,
        dest="num_bombs",
    )

    parser.add_argument(
        "--guide",
        help="Show column and row numbers around the board.",
        action="store_true",
        dest="show_guide",
    )

    args = parser.parse_args(args_list)

    return Configuration(board_size=args.board_size,
                         num_bombs=args.num_bombs,
                         show_guide=args.show_guide)


if __name__ == "__main__":
    config = parse_args(sys.argv[1:])

    game = Game(config=config)
    game.play()
