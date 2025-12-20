from Core.pathfinding import find_path

class Board:
    GRID_SIZE = 9
    MAX_WALLS = 10

    def __init__(self, ai_opponent=False):
        self.ai_opponent = ai_opponent

        self.pawns = {
            "P1": (0, 4),
            "P2": (8, 4)
        }

        # Walls stored as tuples: (x, y, orientation) with orientation "H" or "V"
        self.walls = []

        # Blocked edges stored as frozensets of two positions ((r1, c1), (r2, c2))
        self.blocked_edges = set()

        self.walls_left = {
            "P1": self.MAX_WALLS,
            "P2": self.MAX_WALLS
        }

        self.current_player = "P1"

    def inside_board(self, pos):
        r, c = pos
        return 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE

    def is_adjacent(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    def edge_between(self, a, b):
        # Normalize unordered edge key
        return frozenset((a, b))

    def get_adjacent_positions(self, pos):
        r, c = pos
        return {
            "up": (r - 1, c),
            "down": (r + 1, c),
            "left": (r, c - 1),
            "right": (r, c + 1)
        }

    def _wall_edges_for(self, x, y, o):
        # Return the two blocked edges created by a wall
        if o == "H":
            # Blocks movement between rows x and x+1 along columns y and y+1
            a1, b1 = (x, y), (x + 1, y)
            a2, b2 = (x, y + 1), (x + 1, y + 1)
        else:  # "V"
            # Blocks movement between columns y and y+1 along rows x and x+1
            a1, b1 = (x, y), (x, y + 1)
            a2, b2 = (x + 1, y), (x + 1, y + 1)

        # Only include edges that are within board bounds
        edges = set()
        if self.inside_board(a1) and self.inside_board(b1):
            edges.add(self.edge_between(a1, b1))
        if self.inside_board(a2) and self.inside_board(b2):
            edges.add(self.edge_between(a2, b2))
        return edges

    def is_wall_blocking(self, pos, new_pos):
        # Check if the edge between pos and new_pos is blocked
        return self.edge_between(pos, new_pos) in self.blocked_edges

    def is_jump_move(self, current, opponent, new_pos):
        if not self.is_adjacent(current, opponent):
            return False

        dr = opponent[0] - current[0]
        dc = opponent[1] - current[1]
        jump_pos = (opponent[0] + dr, opponent[1] + dc)

        # Straight jump requires inside board and both edges unblocked:
        # current -> opponent and opponent -> jump_pos
        if new_pos != jump_pos:
            return False
        if not self.inside_board(jump_pos):
            return False
        if self.is_wall_blocking(current, opponent):
            return False
        if self.is_wall_blocking(opponent, jump_pos):
            return False
        return True

    def is_diagonal_move(self, current, opponent, new_pos):
        
        
         
        """
        Diagonal move is allowed ONLY if:
        1. Current pawn is adjacent to opponent
        2. Straight jump over opponent is NOT possible
        3. Diagonal square is valid and inside board
        4. No wall blocks the diagonal path
        """
        
        #  Must be adjacent to opponent
        if not self.is_adjacent(current, opponent):
            return False

        cr, cc = current
        or_, oc = opponent
        nr, nc = new_pos

        dr = or_ - cr
        dc = oc - cc
    # Check if straight jump is possible
        jump_pos = (or_ + dr, oc + dc)
        straight_jump_possible = (
        self.inside_board(jump_pos)
        and not self.is_wall_blocking(current, opponent)
        and not self.is_wall_blocking(opponent, jump_pos)
        )

       # If straight jump is possible → diagonal NOT allowed
        if straight_jump_possible:
            return False

        # 3️⃣ Determine valid diagonal squares
        valid_diagonals = []

        if dr == 0:  # opponent is left or right
        # diagonals are up/down relative to current
         valid_diagonals = [
            (cr - 1, cc + dc),
            (cr + 1, cc + dc)
        ]
        elif dc == 0: 
            # opponent is up or down
        # diagonals are left/right relative to current
             valid_diagonals = [
            (cr + dr, cc - 1),
            (cr + dr, cc + 1)
            ]

    # Target must be one of the valid diagonals
        if new_pos not in valid_diagonals:
            return False

       # Must be inside board
        if not self.inside_board(new_pos):
            return False
        

    # Wall checks
    # Must be able to move from current → opponent
        if self.is_wall_blocking(current, opponent):
            return False

    # Must be able to move from current → diagonal direction
        if self.is_wall_blocking(current, new_pos):
            return False

        return True

    def is_valid_move(self, player, new_pos):
        current = self.pawns[player]
        if not self.inside_board(new_pos):
            return False
        if new_pos == current:
            return False

        opponent_player = "P2" if player == "P1" else "P1"
        opponent = self.pawns[opponent_player]

        # Simple adjacent step (not onto opponent)
        if self.is_adjacent(current, new_pos):
            if new_pos != opponent and not self.is_wall_blocking(current, new_pos):
                return True

        # Straight jump over opponent
        if self.is_jump_move(current, opponent, new_pos):
            return True

        # Diagonal around opponent if straight jump blocked
        if self.is_diagonal_move(current, opponent, new_pos):
            return True

        return False

    def move_pawn(self, player, new_pos):
        if self.is_valid_move(player, new_pos):
            self.pawns[player] = new_pos
            self._switch_turn()
            return True
        return False

    def _crosses_existing_wall(self, x, y, orientation):
        # Prevent crossing at the midpoint
        if orientation == "H":
            # Horizontal at (x, y) crosses vertical at (x, y) or (x, y+1)
            return (x, y, "V") in self.walls or (x, y + 1, "V") in self.walls
        else:  # "V"
            # Vertical at (x, y) crosses horizontal at (x, y) or (x + 1, y)
            return (x, y, "H") in self.walls or (x + 1, y, "H") in self.walls

    def can_place_wall(self, x, y, orientation):
        if orientation not in ("H", "V"):
            return False

        # Walls are placed between squares; top-left anchor must be within 0..GRID-2
        if x < 0 or x >= self.GRID_SIZE - 1 or y < 0 or y >= self.GRID_SIZE - 1:
            return False

        # Exact duplicate
        if (x, y, orientation) in self.walls:
            return False

        # Prevent crossing with existing walls
        if self._crosses_existing_wall(x, y, orientation):
            return False

        # Tentatively add edges and ensure no overlap at the same segment
        new_edges = self._wall_edges_for(x, y, orientation)
        if any(e in self.blocked_edges for e in new_edges):
            # This catches same-segment overlap more robustly
            return False

        # Ensure walls do not completely block paths for either player
        # Simulate placement and run pathfinding
        start_p1 = self.pawns["P1"]
        start_p2 = self.pawns["P2"]
        goals_p1 = [(self.GRID_SIZE - 1, c) for c in range(self.GRID_SIZE)]
        goals_p2 = [(0, c) for c in range(self.GRID_SIZE)]

        # Temporarily modify blocked_edges
        prev_edges = set(self.blocked_edges)
        for e in new_edges:
            self.blocked_edges.add(e)

        try:
            p1_has_path = find_path(start_p1, goals_p1, self.blocked_edges, self.GRID_SIZE) is not None
            p2_has_path = find_path(start_p2, goals_p2, self.blocked_edges, self.GRID_SIZE) is not None
        finally:
            # Revert
            self.blocked_edges = prev_edges

        return p1_has_path and p2_has_path

    def place_wall(self, player, x, y, orientation):
        if self.walls_left[player] <= 0:
            return False

        if self.can_place_wall(x, y, orientation):
            self.walls.append((x, y, orientation))
            for e in self._wall_edges_for(x, y, orientation):
                self.blocked_edges.add(e)
            self.walls_left[player] -= 1
            self._switch_turn()
            return True

        return False

    def copy(self):
        """
        Return a deep copy of the board.
        """
        import copy
        return copy.deepcopy(self)
    def _switch_turn(self):
        self.current_player = "P2" if self.current_player == "P1" else "P1"