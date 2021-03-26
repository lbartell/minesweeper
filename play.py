from lib.game import Game

def main():
    game = Game()

    bombs, flags, counts, visible = game.board.get_states()

    # print("\n\nBombs:")
    # print(bombs)
    # print("\n\nFlags:")
    # print(flags)
    # print("\n\nCounts:")
    # print(counts)

    game.board.show()


if __name__ == "__main__":
    main()