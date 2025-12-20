import copy


class GameState:
    def __init__(self, board):
        # Deep copy everything
        self.pawns = copy.deepcopy(board.pawns)
        self.walls = copy.deepcopy(board.walls)  # store all wall dicts
        self.walls_left = copy.deepcopy(board.walls_left)
        self.current_player = board.current_player

    def restore(self, board):
        board.pawns = copy.deepcopy(self.pawns)
        board.walls = copy.deepcopy(self.walls)
        board.walls_left = copy.deepcopy(self.walls_left)
        board.current_player = self.current_player

