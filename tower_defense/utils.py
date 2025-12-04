"""
Tower Defense Game - Utility Functions
Helper functions used across multiple modules.
"""

import math


def distance(pos1: tuple, pos2: tuple) -> float:
    """Calculate Euclidean distance between two points."""
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.sqrt(dx * dx + dy * dy)


def manhattan_distance(pos1: tuple, pos2: tuple) -> int:
    """Calculate Manhattan distance between two points (used for pathfinding)."""
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b by factor t."""
    return a + (b - a) * t


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def grid_neighbors(x: int, y: int, width: int, height: int, diagonal: bool = False) -> list:
    """
    Get valid neighboring grid positions.
    
    Args:
        x, y: Current grid position
        width, height: Grid dimensions
        diagonal: Whether to include diagonal neighbors
    
    Returns:
        List of valid (x, y) neighbor positions
    """
    neighbors = []
    
    # Cardinal directions
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    # Add diagonal directions if requested
    if diagonal:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append((nx, ny))
    
    return neighbors


def format_time(seconds: float) -> str:
    """Format seconds into MM:SS string."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def format_number(num: int) -> str:
    """Format large numbers with K/M suffixes."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)
