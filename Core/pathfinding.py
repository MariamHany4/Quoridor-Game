from collections import deque

def find_path(start_pos, goal_positions, blocked_edges, grid_size):
    """
    BFS to find a path from start_pos to any of goal_positions.
    Returns a path (list of positions) or None if no path exists.
    """
    queue = deque([(start_pos, [start_pos])])
    visited = set([start_pos])

    while queue:
        pos, path = queue.popleft()
        if pos in goal_positions:
            return path

        r, c = pos
        # 4 orthogonal moves
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for n in neighbors:
            if 0 <= n[0] < grid_size and 0 <= n[1] < grid_size:
                if frozenset((pos, n)) not in blocked_edges and n not in visited:
                    visited.add(n)
                    queue.append((n, path + [n]))

    return None

def shortest_path(player, board_state):
    """
    BFS to find the length of the shortest path from player's pawn to goal row.
    Returns integer distance if path exists, else float('inf').
    """
    start_pos = board_state.pawns[player]
    goal_row = 8 if player == "P1" else 0

    queue = deque([(start_pos, 0)])  # store (position, distance)
    visited = set([start_pos])

    while queue:
        pos, dist = queue.popleft()
        r, c = pos

        if r == goal_row:
            return dist

        for move in board_state.get_adjacent_positions(pos).values():
            if board_state.is_valid_move(player, move) and move not in visited:
                visited.add(move)
                queue.append((move, dist + 1))

    return float('inf')
