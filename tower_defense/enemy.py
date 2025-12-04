"""
Tower Defense Game - Enemy System
Handles enemy types, movement, health, and pathfinding.
"""

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

import math
from typing import List, Tuple, Optional
from config import BASE_ENEMY_HEALTH, BASE_ENEMY_SPEED, TILE_SIZE


class EnemyType:
    """Enum-like class for enemy types."""
    BASIC = "basic"
    FAST = "fast"
    TANK = "tank"


class Enemy:
    """
    Base enemy class that follows paths and can be damaged.
    """

    def __init__(self, path: List[Tuple[int, int]], enemy_type: str = EnemyType.BASIC, wave_number: int = 1):
        # Type and stats
        self.enemy_type = enemy_type
        self.wave_number = wave_number
        self._initialize_stats()

        # Position and movement
        self.path = path  # List of (x, y) grid positions
        self.path_index = 0
        self.x = 0.0  # World position (pixels)
        self.y = 0.0
        self.radius = 6  # Collision radius

        # Set initial position at start of path
        if path:
            start_x, start_y = path[0]
            self.x = start_x * TILE_SIZE + TILE_SIZE // 2
            self.y = start_y * TILE_SIZE + TILE_SIZE // 2

        # Health
        self.max_health = self.base_health
        self.health = self.max_health
        self.alive = True

        # Status effects
        self.slow_multiplier = 1.0  # 1.0 = normal speed, 0.5 = half speed
        self.slow_duration = 0  # Ticks remaining of slow effect

        # Reached end flag
        self.reached_end = False

    def _initialize_stats(self):
        """Initialize enemy stats based on type and wave."""
        # Base stats by type
        if self.enemy_type == EnemyType.BASIC:
            self.base_health = BASE_ENEMY_HEALTH
            self.base_speed = BASE_ENEMY_SPEED
            self.reward = 25
            self.color = (200, 80, 80)  # Red
            self.name = "Basic Enemy"

        elif self.enemy_type == EnemyType.FAST:
            self.base_health = BASE_ENEMY_HEALTH * 0.6  # Less health
            self.base_speed = BASE_ENEMY_SPEED * 1.5  # Faster
            self.reward = 30
            self.color = (80, 200, 80)  # Green
            self.name = "Fast Enemy"

        elif self.enemy_type == EnemyType.TANK:
            self.base_health = BASE_ENEMY_HEALTH * 3  # Much more health
            self.base_speed = BASE_ENEMY_SPEED * 0.7  # Slower
            self.reward = 50
            self.color = (80, 80, 200)  # Blue
            self.name = "Tank Enemy"

        # Scale with wave number
        from config import WAVE_HEALTH_MULTIPLIER, WAVE_SPEED_MULTIPLIER
        self.base_health *= (WAVE_HEALTH_MULTIPLIER ** (self.wave_number - 1))
        self.base_speed *= (WAVE_SPEED_MULTIPLIER ** (self.wave_number - 1))

    def update(self, dt: float = 1.0):
        """
        Update enemy position along path.

        Args:
            dt: Delta time multiplier
        """
        if not self.alive or self.reached_end:
            return

        # Update slow effect
        if self.slow_duration > 0:
            self.slow_duration -= dt
            if self.slow_duration <= 0:
                self.slow_multiplier = 1.0

        # Move along path
        if self.path_index < len(self.path):
            self._move_along_path(dt)

    def _move_along_path(self, dt: float):
        """Move enemy toward next waypoint in path."""
        if self.path_index >= len(self.path):
            self.reached_end = True
            return

        # Get target waypoint (convert grid to world coordinates)
        target_grid_x, target_grid_y = self.path[self.path_index]
        target_x = target_grid_x * TILE_SIZE + TILE_SIZE // 2
        target_y = target_grid_y * TILE_SIZE + TILE_SIZE // 2

        # Calculate direction
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Check if reached waypoint
        if distance < 2:
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.reached_end = True
            return

        # Move toward waypoint
        effective_speed = self.base_speed * self.slow_multiplier * dt
        if distance > 0:
            self.x += (dx / distance) * effective_speed
            self.y += (dy / distance) * effective_speed

    def take_damage(self, damage: int):
        """
        Apply damage to enemy.

        Args:
            damage: Amount of damage to apply
        """
        if not self.alive:
            return

        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def apply_slow(self, slow_multiplier: float, duration: int):
        """
        Apply slow effect to enemy.

        Args:
            slow_multiplier: Speed multiplier (0.5 = half speed)
            duration: Duration in ticks
        """
        self.slow_multiplier = slow_multiplier
        self.slow_duration = duration

    def is_alive(self) -> bool:
        """Check if enemy is alive."""
        return self.alive

    def has_reached_end(self) -> bool:
        """Check if enemy reached the end."""
        return self.reached_end

    def get_health_percentage(self) -> float:
        """Get health as percentage (0.0 to 1.0)."""
        if self.max_health <= 0:
            return 0.0
        return self.health / self.max_health

    def draw(self, surface):
        """Draw the enemy."""
        if not PYGAME_AVAILABLE or not self.alive:
            return

        # Draw enemy circle
        pygame.draw.circle(surface, self.color,
                          (int(self.x), int(self.y)), self.radius)

        # Draw outline
        pygame.draw.circle(surface, (255, 255, 255),
                          (int(self.x), int(self.y)), self.radius, 1)

        # Draw health bar
        self._draw_health_bar(surface)

        # Draw slow effect indicator
        if self.slow_duration > 0:
            # Blue glow for slowed enemies
            glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (100, 150, 255, 80),
                             (self.radius * 2, self.radius * 2), self.radius * 2)
            surface.blit(glow_surface, (int(self.x) - self.radius * 2,
                                       int(self.y) - self.radius * 2))

    def _draw_health_bar(self, surface):
        """Draw health bar above enemy."""
        if not PYGAME_AVAILABLE:
            return

        bar_width = 20
        bar_height = 3
        bar_x = int(self.x - bar_width // 2)
        bar_y = int(self.y - self.radius - 8)

        # Background (red)
        pygame.draw.rect(surface, (100, 0, 0),
                        (bar_x, bar_y, bar_width, bar_height))

        # Health (green)
        health_width = int(bar_width * self.get_health_percentage())
        if health_width > 0:
            pygame.draw.rect(surface, (0, 200, 0),
                            (bar_x, bar_y, health_width, bar_height))

        # Border
        pygame.draw.rect(surface, (255, 255, 255),
                        (bar_x, bar_y, bar_width, bar_height), 1)

    def get_reward(self) -> int:
        """Get money reward for killing this enemy."""
        return self.reward


class EnemySpawner:
    """
    Manages enemy spawning and waves.
    """

    def __init__(self, path: List[Tuple[int, int]]):
        self.path = path
        self.wave_number = 0
        self.enemies_to_spawn = []  # Queue of enemies to spawn
        self.spawn_timer = 0
        self.spawn_interval = 30  # Ticks between spawns (0.5 seconds at 60 FPS)
        self.wave_active = False

    def start_wave(self, wave_number: int):
        """
        Start a new wave of enemies.

        Args:
            wave_number: Wave number (1-indexed)
        """
        self.wave_number = wave_number
        self.wave_active = True
        self.enemies_to_spawn = self._generate_wave(wave_number)
        self.spawn_timer = 0

    def _generate_wave(self, wave_number: int) -> List[str]:
        """
        Generate enemy composition for a wave.

        Args:
            wave_number: Wave number

        Returns:
            List of enemy types to spawn
        """
        enemies = []

        # Wave 1-3: Only basic enemies
        if wave_number <= 3:
            count = 5 + wave_number * 3
            enemies = [EnemyType.BASIC] * count

        # Wave 4-6: Mix of basic and fast
        elif wave_number <= 6:
            basic_count = 5 + wave_number * 2
            fast_count = wave_number - 3
            enemies = [EnemyType.BASIC] * basic_count + [EnemyType.FAST] * fast_count

        # Wave 7+: All types
        else:
            basic_count = 8 + wave_number
            fast_count = wave_number // 2
            tank_count = (wave_number - 6) // 2
            enemies = ([EnemyType.BASIC] * basic_count +
                      [EnemyType.FAST] * fast_count +
                      [EnemyType.TANK] * tank_count)

        return enemies

    def update(self, dt: float = 1.0) -> Optional[Enemy]:
        """
        Update spawner and return next enemy if ready.

        Args:
            dt: Delta time multiplier

        Returns:
            Enemy object if one should spawn, None otherwise
        """
        if not self.wave_active or not self.enemies_to_spawn:
            return None

        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            enemy_type = self.enemies_to_spawn.pop(0)

            # Check if wave complete
            if not self.enemies_to_spawn:
                self.wave_active = False

            return Enemy(self.path, enemy_type, self.wave_number)

        return None

    def is_wave_complete(self) -> bool:
        """Check if current wave spawning is complete."""
        return not self.wave_active and not self.enemies_to_spawn

    def get_remaining_count(self) -> int:
        """Get number of enemies left to spawn in wave."""
        return len(self.enemies_to_spawn)


def create_enemy(path: List[Tuple[int, int]], enemy_type: str = EnemyType.BASIC,
                wave_number: int = 1) -> Enemy:
    """
    Factory function to create an enemy.

    Args:
        path: List of waypoints for enemy to follow
        enemy_type: Type of enemy
        wave_number: Current wave number

    Returns:
        New Enemy instance
    """
    return Enemy(path, enemy_type, wave_number)
