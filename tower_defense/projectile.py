"""
Tower Defense Game - Projectile System
Handles projectile movement, collision detection, and effects.
"""

import pygame
import math
from typing import Optional


class Projectile:
    """
    Projectile fired by towers at enemies.
    """

    def __init__(self, x: float, y: float, target_x: float, target_y: float,
                 speed: float, damage: int, color: tuple = (255, 255, 100)):
        # Position
        self.x = x
        self.y = y

        # Target
        self.target_x = target_x
        self.target_y = target_y

        # Movement
        self.speed = speed
        self.calculate_velocity()

        # Combat
        self.damage = damage
        self.active = True

        # Visual
        self.color = color
        self.radius = 3

    def calculate_velocity(self):
        """Calculate velocity vector toward target."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, dt: float = 1.0):
        """
        Update projectile position.

        Args:
            dt: Delta time multiplier
        """
        if not self.active:
            return

        # Move toward target
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check if reached target (within small threshold)
        dist_to_target = math.sqrt(
            (self.target_x - self.x) ** 2 +
            (self.target_y - self.y) ** 2
        )

        if dist_to_target < self.speed:
            self.active = False

    def draw(self, surface: pygame.Surface):
        """Draw the projectile."""
        if not self.active:
            return

        pygame.draw.circle(surface, self.color,
                          (int(self.x), int(self.y)), self.radius)

        # Draw glow effect
        glow_radius = self.radius + 2
        glow_color = (*self.color, 100)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, glow_color,
                          (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surface,
                    (int(self.x) - glow_radius, int(self.y) - glow_radius))

    def is_active(self) -> bool:
        """Check if projectile is still active."""
        return self.active

    def deactivate(self):
        """Mark projectile as inactive (for pooling)."""
        self.active = False

    def hits_enemy(self, enemy) -> bool:
        """
        Check if projectile hits an enemy.

        Args:
            enemy: Enemy object to check collision with

        Returns:
            True if projectile hits enemy
        """
        if not self.active or not enemy.is_alive():
            return False

        # Simple circle collision
        dist = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
        return dist < (self.radius + enemy.radius)


class ProjectileManager:
    """
    Manages all active projectiles in the game.
    """

    def __init__(self):
        self.projectiles = []

    def add_projectile(self, x: float, y: float, target_x: float, target_y: float,
                      speed: float, damage: int, color: tuple = (255, 255, 100)):
        """
        Add a new projectile.

        Args:
            x, y: Starting position
            target_x, target_y: Target position
            speed: Projectile speed
            damage: Damage dealt on hit
            color: Projectile color (RGB)
        """
        projectile = Projectile(x, y, target_x, target_y, speed, damage, color)
        self.projectiles.append(projectile)

    def update(self, enemies: list, dt: float = 1.0):
        """
        Update all projectiles and check collisions.

        Args:
            enemies: List of enemy objects
            dt: Delta time multiplier
        """
        for projectile in self.projectiles[:]:  # Copy list to allow removal
            if not projectile.is_active():
                self.projectiles.remove(projectile)
                continue

            projectile.update(dt)

            # Check collision with enemies
            for enemy in enemies:
                if projectile.hits_enemy(enemy):
                    enemy.take_damage(projectile.damage)
                    projectile.deactivate()
                    break

    def draw(self, surface: pygame.Surface):
        """Draw all active projectiles."""
        for projectile in self.projectiles:
            projectile.draw(surface)

    def clear(self):
        """Remove all projectiles."""
        self.projectiles.clear()

    def get_count(self) -> int:
        """Get number of active projectiles."""
        return len(self.projectiles)
