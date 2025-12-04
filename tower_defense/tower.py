"""
Tower Defense Game - Tower System
Defines different tower types with shooting and targeting capabilities.
"""

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from typing import Optional, Tuple
from utils import distance


class TowerType:
    """Enum-like class for tower types."""
    WALL = "wall"
    BASIC = "basic"
    SLOW = "slow"
    SNIPER = "sniper"


class Tower:
    """
    Base tower class with shooting, targeting, and upgrade capabilities.
    """

    def __init__(self, grid_x: int, grid_y: int, tower_type: str):
        # Position
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.world_x = 0  # Will be set when placed on grid
        self.world_y = 0

        # Tower type and stats
        self.tower_type = tower_type
        self._initialize_stats()

        # Combat
        self.target = None  # Current enemy being targeted
        self.shoot_cooldown = 0  # Ticks until can shoot again
        self.projectiles = []  # List of active projectiles

        # Visual
        self.angle = 0  # Rotation angle for barrel

    def _initialize_stats(self):
        """Initialize tower stats based on type."""
        if self.tower_type == TowerType.WALL:
            self.range = 0  # No range - just blocks
            self.damage = 0
            self.fire_rate = 0
            self.projectile_speed = 0
            self.cost = 10
            self.color = (80, 80, 90)  # Dark gray
            self.name = "Wall"
            self.description = "Cheap obstacle to guide enemies"

        elif self.tower_type == TowerType.BASIC:
            self.range = 100  # pixels
            self.damage = 10
            self.fire_rate = 60  # ticks between shots (1 second at 60 FPS)
            self.projectile_speed = 5
            self.cost = 100
            self.color = (100, 100, 180)  # Blue
            self.name = "Basic Tower"
            self.description = "Balanced damage and range"

        elif self.tower_type == TowerType.SLOW:
            self.range = 120  # Wider range
            self.damage = 5  # Lower damage
            self.fire_rate = 45  # Faster fire rate
            self.projectile_speed = 6
            self.slow_effect = 0.5  # Slows enemies to 50% speed
            self.slow_duration = 120  # 2 seconds at 60 FPS
            self.cost = 150
            self.color = (80, 180, 180)  # Cyan
            self.name = "Slow Tower"
            self.description = "Slows enemies, wide range"

        elif self.tower_type == TowerType.SNIPER:
            self.range = 200  # Very long range
            self.damage = 50  # High damage
            self.fire_rate = 180  # Slow fire rate (3 seconds)
            self.projectile_speed = 15  # Fast projectiles
            self.cost = 250
            self.color = (180, 100, 100)  # Red
            self.name = "Sniper Tower"
            self.description = "High damage, long range, slow fire"

        else:
            # Default to basic
            self._initialize_stats_for_basic()

    def _initialize_stats_for_basic(self):
        """Fallback to basic tower stats."""
        self.range = 100
        self.damage = 10
        self.fire_rate = 60
        self.projectile_speed = 5
        self.cost = 100
        self.color = (100, 100, 180)
        self.name = "Basic Tower"
        self.description = "Balanced damage and range"

    def set_world_position(self, world_x: int, world_y: int):
        """Set the world position (screen coordinates) of the tower center."""
        self.world_x = world_x
        self.world_y = world_y

    def update(self, enemies: list, dt: float = 1.0):
        """
        Update tower state - targeting, shooting, cooldowns.

        Args:
            enemies: List of enemy objects
            dt: Delta time multiplier (default 1.0 for 60 FPS)
        """
        # Walls don't shoot
        if self.tower_type == TowerType.WALL:
            return

        # Decrease cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        # Find and track target
        self._update_target(enemies)

        # Shoot at target if ready
        if self.target and self.shoot_cooldown <= 0:
            self._shoot()

    def _update_target(self, enemies: list):
        """Find and lock onto the closest enemy in range."""
        # Clear target if it's dead or out of range
        if self.target:
            if not self.target.is_alive():
                self.target = None
            elif not self._is_in_range(self.target):
                self.target = None

        # Find new target if we don't have one
        if not self.target:
            self.target = self._find_closest_enemy(enemies)

        # Update barrel rotation to face target
        if self.target:
            dx = self.target.x - self.world_x
            dy = self.target.y - self.world_y
            import math
            self.angle = math.atan2(dy, dx)

    def _find_closest_enemy(self, enemies: list):
        """Find the closest enemy within range."""
        closest = None
        closest_dist = float('inf')

        for enemy in enemies:
            if not enemy.is_alive():
                continue

            dist = self._distance_to(enemy)
            if dist <= self.range and dist < closest_dist:
                closest = enemy
                closest_dist = dist

        return closest

    def _is_in_range(self, enemy) -> bool:
        """Check if an enemy is within range."""
        return self._distance_to(enemy) <= self.range

    def _distance_to(self, enemy) -> float:
        """Calculate distance to an enemy."""
        return distance((self.world_x, self.world_y), (enemy.x, enemy.y))

    def _shoot(self):
        """Fire a projectile at the current target."""
        if not self.target:
            return

        # Create projectile (will be handled by game state)
        # For now, just apply direct damage and reset cooldown
        self.shoot_cooldown = self.fire_rate

        # Apply damage to target
        self.target.take_damage(self.damage)

        # Apply slow effect if this is a slow tower
        if self.tower_type == TowerType.SLOW and hasattr(self, 'slow_effect'):
            self.target.apply_slow(self.slow_effect, self.slow_duration)

    def draw(self, surface, tile_size: int):
        """
        Draw the tower on the surface.

        Args:
            surface: Pygame surface to draw on
            tile_size: Size of grid tiles (for scaling)
        """
        if not PYGAME_AVAILABLE:
            return

        # Draw base (circle)
        base_radius = tile_size // 3
        pygame.draw.circle(surface, self.color, (self.world_x, self.world_y), base_radius)

        # Draw outline
        pygame.draw.circle(surface, (255, 255, 255), (self.world_x, self.world_y), base_radius, 2)

        # Draw barrel (line pointing at target)
        if self.target:
            import math
            barrel_length = tile_size // 2
            end_x = self.world_x + int(barrel_length * math.cos(self.angle))
            end_y = self.world_y + int(barrel_length * math.sin(self.angle))
            pygame.draw.line(surface, (255, 255, 255),
                           (self.world_x, self.world_y),
                           (end_x, end_y), 3)

    def draw_range(self, surface, alpha: int = 80):
        """
        Draw the tower's range indicator.

        Args:
            surface: Pygame surface to draw on
            alpha: Transparency (0-255)
        """
        if not PYGAME_AVAILABLE:
            return

        # Create transparent surface for range circle
        range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)

        # Draw range circle
        pygame.draw.circle(range_surface, (*self.color, alpha),
                          (self.range, self.range), self.range)

        # Draw range border
        pygame.draw.circle(range_surface, (*self.color, 150),
                          (self.range, self.range), self.range, 2)

        # Blit to main surface (centered on tower)
        surface.blit(range_surface,
                    (self.world_x - self.range, self.world_y - self.range))

    def get_info(self) -> dict:
        """Get tower information for UI display."""
        return {
            'name': self.name,
            'type': self.tower_type,
            'damage': self.damage,
            'range': self.range,
            'fire_rate': self.fire_rate,
            'cost': self.cost,
            'description': self.description,
            'position': (self.grid_x, self.grid_y)
        }

    def get_cost(self) -> int:
        """Get the cost of this tower."""
        return self.cost

    @staticmethod
    def get_tower_cost(tower_type: str) -> int:
        """Get the cost of a tower type without instantiating."""
        costs = {
            TowerType.WALL: 10,
            TowerType.BASIC: 100,
            TowerType.SLOW: 150,
            TowerType.SNIPER: 250
        }
        return costs.get(tower_type, 100)

    @staticmethod
    def get_available_types() -> list:
        """Get list of all available tower types."""
        return [
            {
                'type': TowerType.WALL,
                'name': 'Wall',
                'cost': 10,
                'color': (80, 80, 90),
                'description': 'Cheap obstacle',
                'hotkey': '0'
            },
            {
                'type': TowerType.BASIC,
                'name': 'Basic Tower',
                'cost': 100,
                'color': (100, 100, 180),
                'description': 'Balanced damage and range',
                'hotkey': '1'
            },
            {
                'type': TowerType.SLOW,
                'name': 'Slow Tower',
                'cost': 150,
                'color': (80, 180, 180),
                'description': 'Slows enemies, wide range',
                'hotkey': '2'
            },
            {
                'type': TowerType.SNIPER,
                'name': 'Sniper Tower',
                'cost': 250,
                'color': (180, 100, 100),
                'description': 'High damage, long range',
                'hotkey': '3'
            }
        ]


def create_tower(grid_x: int, grid_y: int, tower_type: str) -> Tower:
    """
    Factory function to create a tower of the specified type.

    Args:
        grid_x: Grid X coordinate
        grid_y: Grid Y coordinate
        tower_type: Type of tower to create

    Returns:
        New Tower instance
    """
    return Tower(grid_x, grid_y, tower_type)
