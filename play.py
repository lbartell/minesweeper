"""
Play a game!
"""
from argparse import ArgumentParser
import sys
from typing import List

from lib.game import Game
from lib.config import Configuration


def parse_args(args_list: List[str]) -> Configuration:
    """Parse arguments"""
    parser = ArgumentParser(description="Minesweeper")

    parser.add_argument(
        "--size",
        "-s",
        help="Board side length, e.g. input 10 for a 10x10 board.",
        type=int,
        dest="board_size",
    )

    parser.add_argument(
        "--bombs",
        "-b",
        help="Number of bombs to place on the board.",
        type=int,
        dest="num_bombs",
    )

    args = parser.parse_args(args_list)
    return Configuration(board_size=args.board_size, num_bombs=args.num_bombs)


if __name__ == "__main__":
    config = parse_args(sys.argv[1:])

    game = Game()
    game.play()
