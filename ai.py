import random


class AI:

    def move(self, board):
        empty_cells = [position for position, symbol in board.items() if symbol == ""]
        return random.choice(empty_cells)