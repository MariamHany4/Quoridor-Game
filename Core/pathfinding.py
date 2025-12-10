from collections import deque

def find_path(player, start_pos, board_state):
    # Set goal row depending on player
    goal_row = 8 if player == "P1" else 0

    # Queue stores tuples: (current_position, path_so_far)
    q = deque()
    q.append((start_pos, [start_pos]))
    
    visited = set()
    visited.add(start_pos)
    
    while q:
        curr_pos, path = q.popleft()
        r, c = curr_pos
        
        # Check if goal is reached
        if r == goal_row:
            return path
        
        # Get possible moves
        moves = board_state.get_adjacent_positions(curr_pos).values()
        for move in moves:
            if board_state.is_valid_move(player, move) and move not in visited:
                visited.add(move)
                q.append((move, path + [move]))
    
    # If queue is empty and goal not reached
    return None
