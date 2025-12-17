from collections import deque


def find_path(start_pos, goals, blocked_edges, grid_size):
    """
    Breadth-first search to find a path from start_pos to any goal square.

    Args:
        start_pos (tuple): (row, col) starting position
        goals (list): list of goal positions [(row, col), ...]
        blocked_edges (set): set of frozenset({pos1, pos2}) representing blocked moves
        grid_size (int): size of the board (usually 9)

    Returns:
        list of positions if path exists, else None
    """
    q = deque()
    q.append((start_pos, [start_pos]))
    visited = {start_pos}

    while q:
        curr_pos, path = q.popleft()
        if curr_pos in goals:
            return path

        r, c = curr_pos
        neighbors = [
            (r - 1, c), (r + 1, c),
            (r, c - 1), (r, c + 1)
        ]

        for move in neighbors:
            if 0 <= move[0] < grid_size and 0 <= move[1] < grid_size:
                edge = frozenset((curr_pos, move))
                if edge not in blocked_edges and move not in visited:
                    visited.add(move)
                    q.append((move, path + [move]))

       