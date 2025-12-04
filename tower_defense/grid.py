"""
Tower Defense Game - Grid System
Handles the game grid, rendering, and cell states.
"""

import pygame
from typing import Optional, List
from config import (
    TILE_SIZE, GRID_WIDTH, GRID_HEIGHT,
    EMPTY, TOWER, WALL, START, END,
    COLORS, CELL_COLORS, DEFAULT_START, DEFAULT_END
)
from pathfinding import Pathfinder
from tower import Tower, create_tower


class Grid:
    """
    Manages the game grid state and rendering.
    """
    
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.tile_size = TILE_SIZE

        # Initialize grid with empty cells
        self.cells = [[EMPTY for _ in range(self.height)] for _ in range(self.width)]

        # Set start and end points
        self.start_pos = DEFAULT_START
        self.end_pos = DEFAULT_END
        self.cells[self.start_pos[0]][self.start_pos[1]] = START
        self.cells[self.end_pos[0]][self.end_pos[1]] = END

        # Create surface for hover overlay (with alpha)
        self.hover_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        # Pathfinding system
        self.pathfinder = Pathfinder(self.width, self.height)
        self.current_path = []
        self._update_path()

        # Tower system
        self.towers = {}  # Dictionary mapping (x, y) -> Tower object
    
    def get_cell(self, grid_x: int, grid_y: int) -> int:
        """Get the state of a cell at grid coordinates."""
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.cells[grid_x][grid_y]
        return -1  # Invalid position
    
    def set_cell(self, grid_x: int, grid_y: int, state: int) -> bool:
        """
        Set the state of a cell. Returns True if successful.
        Prevents modifying start/end points.
        """
        if not (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return False

        # Don't allow modifying start or end points
        if (grid_x, grid_y) == self.start_pos or (grid_x, grid_y) == self.end_pos:
            return False

        self.cells[grid_x][grid_y] = state
        self._update_path()  # Recalculate path when grid changes
        return True
    
    def place_tower(self, grid_x: int, grid_y: int, tower_type: str, game_state) -> bool:
        """
        Place a tower at the given position.

        Args:
            grid_x, grid_y: Grid coordinates
            tower_type: Type of tower to place
            game_state: GameState object to check money

        Returns:
            True if tower was placed, False otherwise
        """
        # Check if position is valid
        if not self.is_valid_placement(grid_x, grid_y):
            return False

        # Check if can afford
        tower_cost = Tower.get_tower_cost(tower_type)
        if not game_state.can_afford(tower_cost):
            return False

        # Check if placing would block path
        if self.would_block_path(grid_x, grid_y):
            return False

        # Create and place tower
        tower = create_tower(grid_x, grid_y, tower_type)

        # Calculate world position (center of tile)
        world_x = grid_x * self.tile_size + self.tile_size // 2
        world_y = grid_y * self.tile_size + self.tile_size // 2
        tower.set_world_position(world_x, world_y)

        # Add to grid
        self.towers[(grid_x, grid_y)] = tower
        self.set_cell(grid_x, grid_y, TOWER)

        # Spend money
        game_state.spend_money(tower_cost)

        return True

    def remove_tower(self, grid_x: int, grid_y: int, game_state) -> bool:
        """
        Remove a tower at the given position.

        Args:
            grid_x, grid_y: Grid coordinates
            game_state: GameState object to refund money

        Returns:
            True if tower was removed, False otherwise
        """
        if (grid_x, grid_y) not in self.towers:
            return False

        # Get tower and refund half the cost
        tower = self.towers[(grid_x, grid_y)]
        refund = tower.get_cost() // 2
        game_state.add_money(refund)

        # Remove tower
        del self.towers[(grid_x, grid_y)]
        self.set_cell(grid_x, grid_y, EMPTY)

        return True

    def get_tower(self, grid_x: int, grid_y: int) -> Optional[Tower]:
        """Get the tower at the given position."""
        return self.towers.get((grid_x, grid_y))

    def get_all_towers(self) -> List[Tower]:
        """Get list of all towers."""
        return list(self.towers.values())

    def update_towers(self, enemies: list, dt: float = 1.0):
        """Update all towers (targeting, shooting)."""
        for tower in self.towers.values():
            tower.update(enemies, dt)
    
    def is_valid_placement(self, grid_x: int, grid_y: int) -> bool:
        """
        Check if a tower can be placed at the given position.
        Includes check for whether placement would block the path.
        """
        if not (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return False

        current = self.get_cell(grid_x, grid_y)
        if current != EMPTY:
            return False

        # Check if placement would block path
        return not self.would_block_path(grid_x, grid_y)
    
    def screen_to_grid(self, screen_x: int, screen_y: int) -> tuple:
        """Convert screen coordinates to grid coordinates."""
        grid_x = screen_x // self.tile_size
        grid_y = screen_y // self.tile_size
        return (grid_x, grid_y)
    
    def grid_to_screen(self, grid_x: int, grid_y: int) -> tuple:
        """Convert grid coordinates to screen coordinates (top-left of cell)."""
        screen_x = grid_x * self.tile_size
        screen_y = grid_y * self.tile_size
        return (screen_x, screen_y)
    
    def draw(self, surface: pygame.Surface, hover_pos: tuple = None, show_path: bool = True,
             show_tower_range: bool = False, selected_tower_pos: tuple = None):
        """
        Render the grid to the given surface.
        hover_pos: Optional grid coordinates for hover highlight.
        show_path: Whether to visualize the current path.
        show_tower_range: Whether to show tower ranges.
        selected_tower_pos: Position of selected tower to show range for.
        """
        # Draw each cell
        for x in range(self.width):
            for y in range(self.height):
                cell_state = self.cells[x][y]
                color = CELL_COLORS.get(cell_state, COLORS['empty'])

                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )

                # Fill cell with color
                pygame.draw.rect(surface, color, rect)

                # Draw grid lines
                pygame.draw.rect(surface, COLORS['grid_line'], rect, 1)

        # Draw path visualization
        if show_path and self.current_path:
            self._draw_path(surface)

        # Draw tower ranges (if enabled)
        if show_tower_range:
            for tower in self.towers.values():
                tower.draw_range(surface)

        # Draw selected tower range
        if selected_tower_pos and selected_tower_pos in self.towers:
            tower = self.towers[selected_tower_pos]
            tower.draw_range(surface, alpha=120)

        # Draw towers
        for tower in self.towers.values():
            tower.draw(surface, self.tile_size)

        # Draw hover highlight
        if hover_pos is not None:
            grid_x, grid_y = hover_pos
            if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                self._draw_hover(surface, grid_x, grid_y)
    
    def _draw_path(self, surface: pygame.Surface):
        """Draw the current path as a line and highlighted cells."""
        if len(self.current_path) < 2:
            return

        # Draw path as highlighted cells (subtle)
        path_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        path_surface.fill((*COLORS['path'], 40))  # Semi-transparent yellow

        for pos in self.current_path:
            # Skip start and end (they have their own colors)
            if pos == self.start_pos or pos == self.end_pos:
                continue

            screen_x, screen_y = self.grid_to_screen(pos[0], pos[1])
            surface.blit(path_surface, (screen_x, screen_y))

        # Draw path as a line connecting cell centers
        points = []
        for pos in self.current_path:
            screen_x, screen_y = self.grid_to_screen(pos[0], pos[1])
            center_x = screen_x + self.tile_size // 2
            center_y = screen_y + self.tile_size // 2
            points.append((center_x, center_y))

        if len(points) >= 2:
            pygame.draw.lines(surface, COLORS['path'], False, points, 3)

    def _draw_hover(self, surface: pygame.Surface, grid_x: int, grid_y: int):
        """Draw hover highlight at the given grid position."""
        # Determine hover color based on whether placement is valid
        if self.is_valid_placement(grid_x, grid_y):
            hover_color = COLORS['hover_valid']
        else:
            hover_color = COLORS['hover_invalid']

        # Create semi-transparent hover overlay
        self.hover_surface.fill(hover_color)

        screen_x, screen_y = self.grid_to_screen(grid_x, grid_y)
        surface.blit(self.hover_surface, (screen_x, screen_y))

        # Draw a brighter border
        rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
        border_color = (255, 255, 255) if self.is_valid_placement(grid_x, grid_y) else (255, 100, 100)
        pygame.draw.rect(surface, border_color, rect, 2)
    
    def draw_debug_info(self, surface: pygame.Surface, font: pygame.font.Font, hover_pos: tuple):
        """Draw debug information (grid coordinates, cell state)."""
        if hover_pos is None:
            return

        grid_x, grid_y = hover_pos
        if not (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return

        cell_state = self.get_cell(grid_x, grid_y)
        state_names = {EMPTY: 'Empty', TOWER: 'Tower', WALL: 'Wall', START: 'Start', END: 'End'}
        state_name = state_names.get(cell_state, 'Unknown')

        debug_text = f"Grid: ({grid_x}, {grid_y}) | State: {state_name}"
        text_surface = font.render(debug_text, True, COLORS['text'])
        surface.blit(text_surface, (10, 10))

        # Show path status
        path_status = f"Path: {'EXISTS' if self.pathfinder.has_path() else 'BLOCKED'} | Length: {len(self.current_path)}"
        path_surface = font.render(path_status, True, COLORS['text'])
        surface.blit(path_surface, (10, 30))

    def _update_path(self):
        """Update the current path using pathfinding."""
        self.pathfinder.update_path(self.cells, self.start_pos, self.end_pos, allow_diagonal=False)
        self.current_path = self.pathfinder.get_path()

    def would_block_path(self, grid_x: int, grid_y: int) -> bool:
        """Check if placing a tower at position would block the path."""
        return self.pathfinder.would_block_path(
            self.cells,
            (grid_x, grid_y),
            self.start_pos,
            self.end_pos,
            allow_diagonal=False
        )

    def get_path(self) -> list:
        """Get the current path from start to end."""
        return self.current_path

    def has_valid_path(self) -> bool:
        """Check if a valid path exists from start to end."""
        return self.pathfinder.has_path()
