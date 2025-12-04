"""
Tower Defense Game - Pathfinding System
Implements A* algorithm for dynamic pathfinding around obstacles.
"""

import heapq
from typing import List, Tuple, Optional, Set
from utils import manhattan_distance, grid_neighbors
from config import EMPTY, TOWER, WALL, START, END


class PathNode:
    """
    Node used in A* pathfinding algorithm.
    """

    def __init__(self, position: Tuple[int, int], g_score: float, h_score: float, parent: Optional['PathNode'] = None):
        self.position = position  # (x, y) grid coordinates
        self.g_score = g_score    # Cost from start to this node
        self.h_score = h_score    # Heuristic cost from this node to goal
        self.f_score = g_score + h_score  # Total cost
        self.parent = parent      # Parent node for path reconstruction

    def __lt__(self, other):
        """Comparison for priority queue (lower f_score = higher priority)."""
        return self.f_score < other.f_score

    def __eq__(self, other):
        """Equality comparison based on position."""
        if not isinstance(other, PathNode):
            return False
        return self.position == other.position

    def __hash__(self):
        """Hash based on position for set operations."""
        return hash(self.position)


class Pathfinder:
    """
    A* pathfinding implementation for tower defense game.
    Finds the shortest path from start to end, avoiding obstacles (towers/walls).
    """

    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.current_path = []  # Cached path as list of (x, y) positions
        self.path_exists = True  # Track if a valid path exists

    def find_path(self, grid_cells: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int],
                  allow_diagonal: bool = False) -> Optional[List[Tuple[int, int]]]:
        """
        Find shortest path from start to goal using A* algorithm.

        Args:
            grid_cells: 2D list representing grid state
            start: Starting position (x, y)
            goal: Goal position (x, y)
            allow_diagonal: Whether to allow diagonal movement

        Returns:
            List of (x, y) positions from start to goal, or None if no path exists
        """
        # Priority queue for open set (nodes to explore)
        open_set = []
        heapq.heappush(open_set, PathNode(start, 0, manhattan_distance(start, goal)))

        # Track visited nodes to avoid reprocessing
        closed_set: Set[Tuple[int, int]] = set()

        # Track best g_score for each position
        g_scores = {start: 0}

        while open_set:
            # Get node with lowest f_score
            current = heapq.heappop(open_set)

            # Check if we reached the goal
            if current.position == goal:
                return self._reconstruct_path(current)

            # Skip if already processed
            if current.position in closed_set:
                continue

            closed_set.add(current.position)

            # Explore neighbors
            x, y = current.position
            neighbors = grid_neighbors(x, y, self.grid_width, self.grid_height, allow_diagonal)

            for neighbor_pos in neighbors:
                # Skip if already processed
                if neighbor_pos in closed_set:
                    continue

                # Skip if blocked (unless it's the goal)
                if not self._is_walkable(grid_cells, neighbor_pos) and neighbor_pos != goal:
                    continue

                # Calculate movement cost (diagonal = 1.414, straight = 1)
                if allow_diagonal:
                    dx = abs(neighbor_pos[0] - current.position[0])
                    dy = abs(neighbor_pos[1] - current.position[1])
                    move_cost = 1.414 if (dx + dy) == 2 else 1.0
                else:
                    move_cost = 1.0

                # Calculate tentative g_score
                tentative_g = current.g_score + move_cost

                # Check if this path to neighbor is better than any previous one
                if neighbor_pos not in g_scores or tentative_g < g_scores[neighbor_pos]:
                    g_scores[neighbor_pos] = tentative_g
                    h_score = manhattan_distance(neighbor_pos, goal)

                    neighbor_node = PathNode(
                        position=neighbor_pos,
                        g_score=tentative_g,
                        h_score=h_score,
                        parent=current
                    )

                    heapq.heappush(open_set, neighbor_node)

        # No path found
        return None

    def _is_walkable(self, grid_cells: List[List[int]], position: Tuple[int, int]) -> bool:
        """
        Check if a position is walkable (not blocked by tower/wall).

        Args:
            grid_cells: 2D list representing grid state
            position: Position to check (x, y)

        Returns:
            True if walkable, False if blocked
        """
        x, y = position

        # Check bounds
        if not (0 <= x < self.grid_width and 0 <= y < self.grid_height):
            return False

        cell_state = grid_cells[x][y]

        # Empty cells, start, and end are walkable
        # Towers and walls are not walkable
        return cell_state in (EMPTY, START, END)

    def _reconstruct_path(self, goal_node: PathNode) -> List[Tuple[int, int]]:
        """
        Reconstruct path from goal node by following parent links.

        Args:
            goal_node: The goal node reached by A*

        Returns:
            List of positions from start to goal
        """
        path = []
        current = goal_node

        while current is not None:
            path.append(current.position)
            current = current.parent

        # Reverse to get path from start to goal
        path.reverse()
        return path

    def update_path(self, grid_cells: List[List[int]], start: Tuple[int, int],
                    goal: Tuple[int, int], allow_diagonal: bool = False) -> bool:
        """
        Update the current cached path.

        Args:
            grid_cells: 2D list representing grid state
            start: Starting position
            goal: Goal position
            allow_diagonal: Whether to allow diagonal movement

        Returns:
            True if path exists, False otherwise
        """
        path = self.find_path(grid_cells, start, goal, allow_diagonal)

        if path is not None:
            self.current_path = path
            self.path_exists = True
            return True
        else:
            self.current_path = []
            self.path_exists = False
            return False

    def get_path(self) -> List[Tuple[int, int]]:
        """Get the current cached path."""
        return self.current_path

    def has_path(self) -> bool:
        """Check if a valid path currently exists."""
        return self.path_exists

    def would_block_path(self, grid_cells: List[List[int]], position: Tuple[int, int],
                         start: Tuple[int, int], goal: Tuple[int, int],
                         allow_diagonal: bool = False) -> bool:
        """
        Check if placing a tower at the given position would block the path.

        Args:
            grid_cells: Current grid state
            position: Position where tower would be placed
            start: Path start position
            goal: Path goal position
            allow_diagonal: Whether to allow diagonal movement

        Returns:
            True if placement would block path, False if path would still exist
        """
        # Make a temporary copy of the grid with the tower placed
        temp_grid = [row[:] for row in grid_cells]
        x, y = position

        # Don't allow placing on start/end
        if temp_grid[x][y] in (START, END):
            return True

        # Temporarily place tower
        original_state = temp_grid[x][y]
        temp_grid[x][y] = TOWER

        # Try to find path with tower placed
        path = self.find_path(temp_grid, start, goal, allow_diagonal)

        # Restore original state
        temp_grid[x][y] = original_state

        # Return True if path was blocked (None returned)
        return path is None


def test_pathfinding():
    """Test the pathfinding implementation."""
    # Create simple 10x10 test grid
    width, height = 10, 10
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]

    start = (1, 5)
    goal = (8, 5)

    grid[start[0]][start[1]] = START
    grid[goal[0]][goal[1]] = END

    # Add some obstacles
    for y in range(2, 8):
        if y != 5:  # Leave gap for path
            grid[5][y] = TOWER

    # Test pathfinding
    pathfinder = Pathfinder(width, height)
    path = pathfinder.find_path(grid, start, goal)

    print("Test Grid (10x10):")
    print("S = Start, E = End, # = Tower, . = Empty")
    print()

    for y in range(height):
        for x in range(width):
            if (x, y) == start:
                print("S", end=" ")
            elif (x, y) == goal:
                print("E", end=" ")
            elif grid[x][y] == TOWER:
                print("#", end=" ")
            elif path and (x, y) in path:
                print("*", end=" ")
            else:
                print(".", end=" ")
        print()

    print()
    if path:
        print(f"Path found! Length: {len(path)}")
        print(f"Path: {path}")
    else:
        print("No path found!")

    # Test blocking
    print("\nTesting path blocking...")
    blocking_pos = (4, 5)
    would_block = pathfinder.would_block_path(grid, blocking_pos, start, goal)
    print(f"Placing tower at {blocking_pos} would block path: {would_block}")


if __name__ == "__main__":
    test_pathfinding()
