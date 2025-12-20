import copy
import random
import sys
import os
import importlib.util
from . import heuristics
from . import minimax
# Dynamic import for pathfinding in Core folder
pathfinding_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Core', 'pathfinding.py'))
import importlib.util
spec = importlib.util.spec_from_file_location("pathfinding", pathfinding_path)
pathfinding = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pathfinding)


class AIPlayer:
    def __init__(self, player, difficulty="easy"):
        self.player = player
        self.opponent = "P2" if player == "P1" else "P1"
        self.difficulty = difficulty

        # Depth based on difficulty
        if difficulty == "easy":
            self.depth = 1
        elif difficulty == "medium":
            self.depth = 2
        elif difficulty == "hard":
            self.depth = 3
        else:
            self.depth = 1  # default easy


    def choose_action(self, board):
        actions = self._generate_all_actions(board)

        if self.difficulty == "easy":
            return self._choose_greedy(board, actions)

        # Medium and Hard: minimax with alpha-beta
        best_score = float("-inf") if self.player == "P1" else float("inf")
        best_action = None
        alpha = float('-inf')
        beta = float('inf')

        for action in actions:
            simulated_board = self._simulate_action(board, action)
            score = minimax.minimax_alpha_beta_quoridor(
                simulated_board,
                depth=self.depth - 1,
                is_maximizing=(self.player == "P2"),  # opponent's turn
                alpha=alpha,
                beta=beta
            )

            if self.player == "P1":
                if score > best_score:
                    best_score = score
                    best_action = action
                    alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_action = action
                    beta = min(beta, best_score)

        return best_action

    # greedy heuristic for easy 
    def _choose_greedy(self, board, actions):
        best_score = float("-inf")
        best_actions = []

        for action in actions:
            simulated_board = self._simulate_action(board, action)
            score = heuristics.heuristic(simulated_board)

            if score > best_score:
                best_score = score
                best_actions = [action]
            elif score == best_score:
                best_actions.append(action)

        return random.choice(best_actions)


    def _generate_all_actions(self, board):
        return self._generate_pawn_moves(board) + self._generate_wall_moves(board)

    def _generate_pawn_moves(self, board):
        moves = []
        current_pos = board.pawns[self.player]
        opponent_pos = board.pawns[self.opponent]

        for new_pos in board.get_adjacent_positions(current_pos).values():
            if board.is_valid_move(self.player, new_pos):
                moves.append({"type": "move", "to": new_pos})

        return moves

    def _generate_wall_moves(self, board):
        moves = []
        if board.walls_left[self.player] <= 0:
            return moves

        for x in range(board.GRID_SIZE - 1):
            for y in range(board.GRID_SIZE - 1):
                for orientation in ("H", "V"):
                    if board.can_place_wall(x, y, orientation):
                        moves.append({
                            "type": "wall",
                            "x": x,
                            "y": y,
                            "orientation": orientation
                        })
        return moves


    def _simulate_action(self, board, action):
        new_board = copy.deepcopy(board)

        if action["type"] == "move":
            new_board.move_pawn(self.player, action["to"])
        else:
            new_board.place_wall(
                self.player,
                action["x"],
                action["y"],
                action["orientation"]
            )

        return new_board


    # checking that wall does not block paths
    def _wall_keeps_paths(self, board, x, y, orientation):
        test_board = copy.deepcopy(board)
        test_board.place_wall(self.player, x, y, orientation)

        ai_path_length = pathfinding.shortest_path(self.player, test_board)
        opp_path_length = pathfinding.shortest_path(self.opponent, test_board)

        return ai_path_length != float('inf') and opp_path_length != float('inf')
