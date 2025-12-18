from Ai.heuristics import heuristic
#=====================================================
# Minimax algorithm
#======================================================
def is_game_over(board):
    """
    Check if the game is over.
    P1 wins if reaches column 8
    P2 wins if reaches column 0
    """
    # P1 reached last column (column 8)
    if board.pawns["P1"][1] == 8:
        return True

    # P2 reached first column (column 0)
    if board.pawns["P2"][1] == 0:
        return True

    return False


def check_winner(board):
    """
    Separate function to check winner (returns string)
    """
    if board.pawns["P1"][1] == 8:
        return "P1 is winner"
    elif board.pawns["P2"][1] == 0:
        return "P2 is winner"
    else:
        return "Game not over"


def minimax_alpha_beta_quoridor(board, depth, is_maximizing,alpha,beta):
    """
    Minimax algorithm for Quoridor
    """
    # Base case - game is over
    if is_game_over(board):
        if board.pawns["P1"][1] == 8:
            return 10000
        elif board.pawns["P2"][1] == 0:
            return -10000

    # Base case - depth limit reached
    if depth == 0:
        return heuristic(board)

    # Maximizer (P1's turn)
    if is_maximizing:
        max_value = float('-inf')
        moves = get_possible_moves(board, "P1")

        for move in moves:
            new_board = board.copy()
            apply_move(new_board, move, "P1")
            value = minimax_alpha_beta_quoridor(new_board, depth - 1, False,alpha,beta)
            max_value = max(max_value, value)

            alpha =max(alpha, value)
            if beta<=alpha:
                break

        return max_value

    # Minimizer (P2's turn)
    else:
        min_value = float('inf')
        moves = get_possible_moves(board, "P2")

        for move in moves:
            new_board = board.copy()
            apply_move(new_board, move, "P2")
            value = minimax_alpha_beta_quoridor(new_board, depth - 1, True,alpha,beta)
            min_value = min(min_value, value)
            beta = min(beta,value)
            if beta<=alpha:
                break

        return min_value


def get_possible_moves(board, player):
    """
    Returns list of all possible moves for a player
    """
    moves = []

    # 1. Pawn moves
    current_pos = board.pawns[player]
    for direction, new_pos in board.get_adjacent_positions(current_pos).items():
        if board.is_valid_move(player, new_pos):
            moves.append(('move', new_pos))

    # 2. Wall placements
    if board.walls_left[player] > 0:
        for x in range(board.GRID_SIZE - 1):
            for y in range(board.GRID_SIZE - 1):
                if board.can_place_wall(x, y, 'H'):
                    moves.append(('wall', x, y, 'H'))

                if board.can_place_wall(x, y, 'V'):
                    moves.append(('wall', x, y, 'V'))

    return moves


def apply_move(board, move, player):
    """
    Apply a move to the board
    """
    if move[0] == 'move':
        _, new_pos = move
        board.move_pawn(player, new_pos)

    elif move[0] == 'wall':
        _, x, y, orientation = move
        board.place_wall(player, x, y, orientation)

############################# AI player #########################
def get_best_move(board, player, difficulty="medium"):
    """
    Find the best move for the player using Minimax

    Args:
        board: current Board state
        player: "P1" or "P2"
        difficulty: "easy", "medium", "hard", "expert"

    Returns:
        best_move: the best move to make
        best_score: the score of that move
    """
    # Set depth based on difficulty
    if difficulty == "easy":
        depth = 1  # Very fast, weak AI
    elif difficulty == "medium":
        depth = 3  # Balanced
    elif difficulty == "hard":
        depth = 4  # Strong, a bit slower
    elif difficulty == "expert":
        depth = 5  # Very strong, slower
    else:
        depth = 3  # Default to medium

    # Determine if maximizing or minimizing
    is_maximizing = (player == "P1")

    # Initialize best value
    if is_maximizing:
        best_value = float('-inf')
    else:
        best_value = float('inf')

    best_move = None

    # Get all possible moves
    possible_moves = get_possible_moves(board, player)

    # Initialize alpha and beta
    alpha = float('-inf')
    beta = float('inf')

    # Try each move
    for move in possible_moves:
        # Copy board and apply move
        new_board = board.copy()
        apply_move(new_board, move, player)

        # Evaluate this move using minimax
        value = minimax_alpha_beta_quoridor(new_board, depth - 1, not is_maximizing,alpha,beta)

        # Update best move if better
        if is_maximizing:
            if value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, best_value)  # Update alpha
        else:
            if value < best_value:
                best_value = value
                best_move = move
                beta = min(beta, best_value)  # Update alpha

    return best_move, best_value