
import heapq
def a_star_heuristic(curr_pos, goal_row):
    """
    Manhattan distance to the target row.
    curr_pos = (r, c)
    goal_row = integer row the player must reach
    """
    r, c = curr_pos
    return abs(r - goal_row)



def shortest_path(board, player):
    """
    A* shortest path for a player's pawn to its goal line.
    Returns length of shortest path.
    """

    start = board.pawns[player]
    goal_row = 8 if player == "P1" else 0  # P1 goes DOWN, P2 goes UP

    visited = set()
    pq = []  # priority queue

    # (f_score, g_score, position)
    heapq.heappush(pq, (a_star_heuristic(start, goal_row), 0, start))

    while pq:
        f_score, g_score, pos = heapq.heappop(pq)

        if pos in visited:
            continue
        visited.add(pos)

        r, c = pos

        # Reached goal row
        if r == goal_row:
            return g_score

        # Expand neighbors
        for move in board.get_adjacent_positions(pos).values():
            if not board.inside_board(move):
                continue
            if board.is_wall_blocking(pos, move):
                continue
                   
            if move not in visited:
                new_g = g_score + 1
                new_f = new_g + a_star_heuristic(move, goal_row)
                heapq.heappush(pq, (new_f, new_g, move))

    # No path found (should never happen if walls allow path)
    return float('inf')

def heuristic(board):
    """
    Evaluate board state for AI.
    Higher score = better for P1 (AI if AI is P1).
    """

    p1_dist = shortest_path(board, "P1")
    p2_dist = shortest_path(board, "P2")

    # Basic heuristic: difference in path length
    score = (p2_dist - p1_dist) * 10

    # Mobility bonus
    p1_moves = 0
    p2_moves = 0

    for m in board.get_adjacent_positions(board.pawns["P1"]).values():
        if board.inside_board(m) and not board.is_wall_blocking(board.pawns["P1"], m):
            p1_moves += 1

    for m in board.get_adjacent_positions(board.pawns["P2"]).values():
        if board.inside_board(m) and not board.is_wall_blocking(board.pawns["P2"], m):
            p2_moves += 1

    score += (p1_moves - p2_moves) * 0.5

    # Wall advantage
    score += (board.walls_left["P1"] - board.walls_left["P2"]) * 1.0

    return score