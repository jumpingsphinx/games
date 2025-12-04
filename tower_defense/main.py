"""
Tower Defense Game - Main Entry Point
Phase 4: Enemy Mechanics - Enemies, Waves, and Combat
"""

import pygame
import sys
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    COLORS, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, UI_PANEL_HEIGHT
)
from grid import Grid
from game_state import GameState
from tower import TowerType, Tower
from enemy import EnemySpawner


class Game:
    """
    Main game class handling the game loop, input, and rendering.
    """
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        # Calculate actual window size based on grid + UI
        self.window_width = GRID_WIDTH * TILE_SIZE
        self.window_height = GRID_HEIGHT * TILE_SIZE + UI_PANEL_HEIGHT

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)

        # Game state
        self.running = True
        self.game_state = GameState()

        # Grid system
        self.grid = Grid()

        # Enemy system
        self.enemies = []  # List of active enemies
        self.enemy_spawner = EnemySpawner(self.grid.current_path)

        # Mouse state
        self.hover_pos = None  # Current grid position under mouse
        self.mouse_held = False

        # Tower selection
        self.selected_tower_type = TowerType.BASIC
        self.selected_tower_pos = None  # Grid position of selected tower for info
        self.show_tower_ranges = False

        # Debug/info display
        self.show_debug = True
        self.show_path = True  # Toggle path visualization
    
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
            self.game_state.toggle_pause()

        elif event.key == pygame.K_d:
            self.show_debug = not self.show_debug

        elif event.key == pygame.K_v:
            # Toggle path visualization
            self.show_path = not self.show_path

        elif event.key == pygame.K_t:
            # Toggle tower range visualization
            self.show_tower_ranges = not self.show_tower_ranges

        elif event.key == pygame.K_r:
            # Reset grid (keep start/end, clear towers)
            self._reset_grid()

        elif event.key == pygame.K_SPACE:
            # Start next wave
            self._start_next_wave()

        # Tower selection hotkeys
        elif event.key == pygame.K_0:
            self.selected_tower_type = TowerType.WALL
        elif event.key == pygame.K_1:
            self.selected_tower_type = TowerType.BASIC
        elif event.key == pygame.K_2:
            self.selected_tower_type = TowerType.SLOW
        elif event.key == pygame.K_3:
            self.selected_tower_type = TowerType.SNIPER
    
    def _handle_mouse_motion(self, event):
        """Handle mouse movement."""
        mouse_x, mouse_y = event.pos
        # Adjust for UI panel at top
        grid_mouse_y = mouse_y - UI_PANEL_HEIGHT
        if grid_mouse_y >= 0:
            self.hover_pos = self.grid.screen_to_grid(mouse_x, grid_mouse_y)
        else:
            self.hover_pos = None
    
    def _handle_mouse_down(self, event):
        """Handle mouse button press."""
        if event.button == 1:  # Left click
            self.mouse_held = True
            if self.hover_pos:
                grid_x, grid_y = self.hover_pos
                # Try to place selected tower type
                placed = self.grid.place_tower(grid_x, grid_y, self.selected_tower_type, self.game_state)
                if not placed and self.grid.get_tower(grid_x, grid_y):
                    # If couldn't place and there's a tower, select it
                    self.selected_tower_pos = (grid_x, grid_y)

        elif event.button == 3:  # Right click
            # Remove tower and get refund
            if self.hover_pos:
                grid_x, grid_y = self.hover_pos
                self.grid.remove_tower(grid_x, grid_y, self.game_state)
                if self.selected_tower_pos == (grid_x, grid_y):
                    self.selected_tower_pos = None
    
    def _handle_mouse_up(self, event):
        """Handle mouse button release."""
        if event.button == 1:
            self.mouse_held = False
    
    def _reset_grid(self):
        """Reset the grid to initial state."""
        self.grid = Grid()
        self.enemies.clear()
        self.enemy_spawner = EnemySpawner(self.grid.current_path)
        self.game_state.reset()

    def _start_next_wave(self):
        """Start the next wave of enemies."""
        if self.game_state.wave_active:
            return  # Wave already active

        next_wave = self.game_state.current_wave + 1
        self.game_state.start_wave(next_wave, 0)  # Enemy count updated by spawner
        self.enemy_spawner.start_wave(next_wave)

        # Update path for spawner in case towers changed
        self.enemy_spawner.path = self.grid.current_path

    def update(self):
        """Update game state."""
        if self.game_state.is_paused() or self.game_state.is_game_over():
            return

        # Spawn enemies
        new_enemy = self.enemy_spawner.update(dt=1.0)
        if new_enemy:
            self.enemies.append(new_enemy)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt=1.0)

            # Check if enemy reached end
            if enemy.has_reached_end():
                self.game_state.lose_life()
                self.enemies.remove(enemy)
                continue

            # Remove dead enemies and award money
            if not enemy.is_alive():
                self.game_state.add_kill()
                self.enemies.remove(enemy)

        # Update towers (targeting and shooting)
        self.grid.update_towers(self.enemies, dt=1.0)

        # Check if wave complete
        if (self.game_state.wave_active and
            self.enemy_spawner.is_wave_complete() and
            len(self.enemies) == 0):
            self.game_state.wave_complete()
    
    def draw(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(COLORS['background'])

        # Create surface for grid area (offset by UI panel height)
        grid_surface = self.screen.subsurface(pygame.Rect(0, UI_PANEL_HEIGHT,
                                                          self.window_width,
                                                          GRID_HEIGHT * TILE_SIZE))

        # Draw grid with hover highlight and optional path visualization
        self.grid.draw(grid_surface, self.hover_pos,
                      show_path=self.show_path,
                      show_tower_range=self.show_tower_ranges,
                      selected_tower_pos=self.selected_tower_pos)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(grid_surface)

        # Draw UI panel at top
        self._draw_ui_panel()

        # Draw debug info
        if self.show_debug:
            self._draw_debug_info()
            self._draw_controls_info()

        # Draw pause overlay
        if self.game_state.is_paused():
            self._draw_pause_overlay()

        # Update display
        pygame.display.flip()
    
    def _draw_ui_panel(self):
        """Draw the top UI panel with money, lives, and tower selection."""
        # Background panel
        panel_rect = pygame.Rect(0, 0, self.window_width, UI_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, (40, 40, 50), panel_rect)
        pygame.draw.line(self.screen, (100, 100, 110),
                        (0, UI_PANEL_HEIGHT), (self.window_width, UI_PANEL_HEIGHT), 2)

        # Game stats (left side)
        stats_x = 15
        stats_y = 15

        money_text = self.font.render(f"Money: ${self.game_state.money}", True, (100, 255, 100))
        self.screen.blit(money_text, (stats_x, stats_y))

        lives_text = self.font.render(f"Lives: {self.game_state.lives}", True, (255, 100, 100))
        self.screen.blit(lives_text, (stats_x, stats_y + 25))

        # Wave info
        wave_text = f"Wave: {self.game_state.current_wave}"
        if self.game_state.wave_active:
            wave_text += f" ({len(self.enemies)} enemies)"
        else:
            wave_text += " (SPACE to start)"
        wave_surface = self.small_font.render(wave_text, True, (200, 200, 100))
        self.screen.blit(wave_surface, (stats_x, stats_y + 50))

        # Tower selection (center/right)
        tower_x = 250
        tower_y = 10

        label = self.small_font.render("Select Tower:", True, COLORS['text'])
        self.screen.blit(label, (tower_x, tower_y))

        # Draw tower type buttons
        tower_types = Tower.get_available_types()
        button_width = 120
        button_height = 50
        button_spacing = 10

        for i, tower_info in enumerate(tower_types):
            x = tower_x + i * (button_width + button_spacing)
            y = tower_y + 20

            # Button background
            is_selected = (tower_info['type'] == self.selected_tower_type)
            border_color = (255, 255, 255) if is_selected else (100, 100, 110)
            border_width = 3 if is_selected else 1

            button_rect = pygame.Rect(x, y, button_width, button_height)
            pygame.draw.rect(self.screen, tower_info['color'], button_rect)
            pygame.draw.rect(self.screen, border_color, button_rect, border_width)

            # Tower name
            name_text = self.small_font.render(tower_info['name'], True, COLORS['text'])
            name_rect = name_text.get_rect(center=(x + button_width // 2, y + 15))
            self.screen.blit(name_text, name_rect)

            # Cost
            cost_text = self.small_font.render(f"${tower_info['cost']}", True, (100, 255, 100))
            cost_rect = cost_text.get_rect(center=(x + button_width // 2, y + 32))
            self.screen.blit(cost_text, cost_rect)

            # Hotkey
            hotkey_text = self.small_font.render(f"[{tower_info['hotkey']}]", True, (200, 200, 200))
            self.screen.blit(hotkey_text, (x + 2, y + 2))

    def _draw_debug_info(self):
        """Draw debug information."""
        if not self.hover_pos:
            return

        grid_x, grid_y = self.hover_pos
        if not (0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT):
            return

        debug_y = UI_PANEL_HEIGHT + 10
        cell_state = self.grid.get_cell(grid_x, grid_y)
        state_names = {0: 'Empty', 1: 'Tower', 2: 'Wall', 3: 'Start', 4: 'End'}
        state_name = state_names.get(cell_state, 'Unknown')

        debug_text = f"Grid: ({grid_x}, {grid_y}) | State: {state_name}"
        text_surface = self.font.render(debug_text, True, COLORS['text'])
        self.screen.blit(text_surface, (10, debug_y))

        # Show path status
        path_status = f"Path: {'EXISTS' if self.grid.pathfinder.has_path() else 'BLOCKED'} | Length: {len(self.grid.current_path)}"
        path_surface = self.font.render(path_status, True, COLORS['text'])
        self.screen.blit(path_surface, (10, debug_y + 20))

        # Show selected tower info
        if self.selected_tower_pos:
            tower = self.grid.get_tower(*self.selected_tower_pos)
            if tower:
                info = tower.get_info()
                tower_text = f"Selected: {info['name']} | Dmg: {info['damage']} | Range: {info['range']}"
                tower_surface = self.font.render(tower_text, True, COLORS['text'])
                self.screen.blit(tower_surface, (10, debug_y + 40))

    def _draw_controls_info(self):
        """Draw control instructions."""
        controls = [
            "Controls:",
            "SPACE - Start Wave | Left Click - Place | Right Click - Remove",
            "0 - Wall ($10) | 1/2/3 - Towers | P - Pause | T - Ranges",
            "V - Path | D - Debug | R - Reset | ESC - Quit"
        ]

        y_offset = self.window_height - len(controls) * 18 - 10
        for i, line in enumerate(controls):
            text_surface = self.small_font.render(line, True, COLORS['text'])
            self.screen.blit(text_surface, (10, y_offset + i * 18))
    
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
    print("=" * 60)
    print("Tower Defense Game - Phase 4: Enemy Mechanics")
    print("=" * 60)
    print("\nInitializing game...")

    game = Game()

    print("Game started!")
    print("\nControls:")
    print("  SPACE       - Start next wave")
    print("  Left Click  - Place selected tower")
    print("  Right Click - Remove tower (50% refund)")
    print("  0/1/2/3     - Select tower type")
    print("  P           - Pause game")
    print("  D           - Toggle debug info")
    print("  V           - Toggle path visualization")
    print("  T           - Toggle tower ranges")
    print("  R           - Reset grid")
    print("  ESC         - Quit game")
    print("\nTower Types:")
    print("  [0] Wall         - $10   - Cheap obstacle")
    print("  [1] Basic Tower  - $100  - Balanced")
    print("  [2] Slow Tower   - $150  - Slows enemies")
    print("  [3] Sniper Tower - $250  - High damage, long range")
    print("\nEnemy Types:")
    print("  Basic (Red)   - Normal speed, normal health")
    print("  Fast (Green)  - Fast speed, less health")
    print("  Tank (Blue)   - Slow speed, lots of health")
    print("\nFeatures:")
    print("  - Wave system with increasing difficulty")
    print("  - 3 enemy types")
    print("  - Tower-enemy combat")
    print("  - Economy system ($500 starting, 20 lives)")
    print("  - Dynamic pathfinding")
    print()

    game.run()


if __name__ == "__main__":
    main()
