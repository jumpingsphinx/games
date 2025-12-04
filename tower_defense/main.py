"""
Tower Defense Game - Main Entry Point
Phase 1: Foundation - Window, Grid, and Mouse Interaction
"""

import pygame
import sys
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    COLORS, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT
)
from grid import Grid


class Game:
    """
    Main game class handling the game loop, input, and rendering.
    """
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        # Calculate actual window size based on grid
        self.window_width = GRID_WIDTH * TILE_SIZE
        self.window_height = GRID_HEIGHT * TILE_SIZE
        
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        
        # Game state
        self.running = True
        self.paused = False
        
        # Grid system
        self.grid = Grid()
        
        # Mouse state
        self.hover_pos = None  # Current grid position under mouse
        self.mouse_held = False
        
        # Debug/info display
        self.show_debug = True
    
    def handle_events(self):
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event)
    
    def _handle_keydown(self, event):
        """Handle keyboard input."""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        
        elif event.key == pygame.K_p:
            self.paused = not self.paused
        
        elif event.key == pygame.K_d:
            self.show_debug = not self.show_debug
        
        elif event.key == pygame.K_r:
            # Reset grid (keep start/end, clear towers)
            self._reset_grid()
    
    def _handle_mouse_motion(self, event):
        """Handle mouse movement."""
        mouse_x, mouse_y = event.pos
        self.hover_pos = self.grid.screen_to_grid(mouse_x, mouse_y)
    
    def _handle_mouse_down(self, event):
        """Handle mouse button press."""
        if event.button == 1:  # Left click
            self.mouse_held = True
            if self.hover_pos:
                grid_x, grid_y = self.hover_pos
                self.grid.toggle_tower(grid_x, grid_y)
        
        elif event.button == 3:  # Right click
            # Could be used for tower removal or other actions
            if self.hover_pos:
                grid_x, grid_y = self.hover_pos
                current = self.grid.get_cell(grid_x, grid_y)
                if current == 1:  # TOWER
                    self.grid.set_cell(grid_x, grid_y, 0)  # EMPTY
    
    def _handle_mouse_up(self, event):
        """Handle mouse button release."""
        if event.button == 1:
            self.mouse_held = False
    
    def _reset_grid(self):
        """Reset the grid to initial state."""
        self.grid = Grid()
    
    def update(self):
        """Update game state."""
        if self.paused:
            return
        
        # Future: Update enemies, projectiles, etc.
        pass
    
    def draw(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(COLORS['background'])
        
        # Draw grid with hover highlight
        self.grid.draw(self.screen, self.hover_pos)
        
        # Draw debug info
        if self.show_debug:
            self.grid.draw_debug_info(self.screen, self.font, self.hover_pos)
            self._draw_controls_info()
        
        # Draw pause overlay
        if self.paused:
            self._draw_pause_overlay()
        
        # Update display
        pygame.display.flip()
    
    def _draw_controls_info(self):
        """Draw control instructions."""
        controls = [
            "Controls:",
            "Left Click - Place/Remove Tower",
            "Right Click - Remove Tower",
            "P - Pause | D - Toggle Debug",
            "R - Reset Grid | ESC - Quit"
        ]
        
        y_offset = self.window_height - len(controls) * 20 - 10
        for i, line in enumerate(controls):
            text_surface = self.font.render(line, True, COLORS['text'])
            self.screen.blit(text_surface, (10, y_offset + i * 20))
    
    def _draw_pause_overlay(self):
        """Draw pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.large_font.render("PAUSED", True, COLORS['text'])
        text_rect = pause_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.screen.blit(pause_text, text_rect)
        
        # Instructions
        resume_text = self.font.render("Press P to resume", True, COLORS['text'])
        resume_rect = resume_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 40))
        self.screen.blit(resume_text, resume_rect)
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    print("=" * 50)
    print("Tower Defense Game - Phase 1: Foundation")
    print("=" * 50)
    print("\nInitializing game...")
    
    game = Game()
    
    print("Game started!")
    print("\nControls:")
    print("  Left Click  - Place/Remove tower")
    print("  Right Click - Remove tower")
    print("  P           - Pause game")
    print("  D           - Toggle debug info")
    print("  R           - Reset grid")
    print("  ESC         - Quit game")
    print()
    
    game.run()


if __name__ == "__main__":
    main()
