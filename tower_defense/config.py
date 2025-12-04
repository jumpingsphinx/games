"""
Tower Defense Game - Configuration and Constants
"""

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
TITLE = "Tower Defense - Dynamic Pathfinding"

# Grid settings
TILE_SIZE = 20
GRID_WIDTH = 40   # Number of tiles horizontally
GRID_HEIGHT = 30  # Number of tiles vertically

# Grid states
EMPTY = 0
TOWER = 1
WALL = 2
START = 3
END = 4

# Colors (RGB)
COLORS = {
    'background': (30, 30, 40),
    'grid_line': (50, 50, 60),
    'empty': (40, 40, 50),
    'tower': (100, 100, 180),
    'wall': (60, 60, 70),
    'start': (80, 180, 80),
    'end': (180, 80, 80),
    'hover': (255, 255, 255, 80),
    'hover_valid': (80, 180, 80, 100),
    'hover_invalid': (180, 80, 80, 100),
    'path': (255, 200, 50),
    'text': (220, 220, 220),
}

# Map cell type to color
CELL_COLORS = {
    EMPTY: COLORS['empty'],
    TOWER: COLORS['tower'],
    WALL: COLORS['wall'],
    START: COLORS['start'],
    END: COLORS['end'],
}

# Default start and end positions (grid coordinates)
DEFAULT_START = (2, 15)
DEFAULT_END = (37, 15)

# UI settings
UI_HEIGHT = 0  # Reserved space at top for UI (Phase 6)
