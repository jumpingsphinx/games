"""
Tower Defense Game - Grid System
Handles the game grid, rendering, and cell states.
"""

import pygame
from config import (
    TILE_SIZE, GRID_WIDTH, GRID_HEIGHT,
    EMPTY, TOWER, WALL, START, END,
    COLORS, CELL_COLORS, DEFAULT_START, DEFAULT_END
)


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
        return True
    
    def toggle_tower(self, grid_x: int, grid_y: int) -> bool:
        """
        Toggle a tower at the given position.
        Returns True if tower was placed, False if removed or invalid.
        """
        current = self.get_cell(grid_x, grid_y)
        
        if current == EMPTY:
            return self.set_cell(grid_x, grid_y, TOWER)
        elif current == TOWER:
            self.set_cell(grid_x, grid_y, EMPTY)
            return False
        
        return False
    
    def is_valid_placement(self, grid_x: int, grid_y: int) -> bool:
        """Check if a tower can be placed at the given position."""
        if not (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return False
        
        current = self.get_cell(grid_x, grid_y)
        return current == EMPTY
    
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
    
    def draw(self, surface: pygame.Surface, hover_pos: tuple = None):
        """
        Render the grid to the given surface.
        hover_pos: Optional grid coordinates for hover highlight.
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
        
        # Draw hover highlight
        if hover_pos is not None:
            grid_x, grid_y = hover_pos
            if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                self._draw_hover(surface, grid_x, grid_y)
    
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
