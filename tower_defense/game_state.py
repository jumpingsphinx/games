"""
Tower Defense Game - Game State Management
Manages money, lives, score, waves, and game progression.
"""

from config import STARTING_MONEY, STARTING_LIVES, ENEMY_KILL_REWARD


class GameState:
    """
    Manages the overall game state including resources, score, and waves.
    """

    def __init__(self):
        # Resources
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES

        # Score
        self.score = 0
        self.kills = 0

        # Wave system (for Phase 4)
        self.current_wave = 0
        self.wave_active = False
        self.enemies_in_wave = 0
        self.enemies_spawned = 0

        # Game status
        self.game_over = False
        self.game_won = False
        self.paused = False

    def can_afford(self, cost: int) -> bool:
        """Check if player has enough money."""
        return self.money >= cost

    def spend_money(self, cost: int) -> bool:
        """
        Attempt to spend money.

        Args:
            cost: Amount to spend

        Returns:
            True if purchase successful, False if not enough money
        """
        if self.can_afford(cost):
            self.money -= cost
            return True
        return False

    def add_money(self, amount: int):
        """Add money to player's total."""
        self.money += amount
        self.score += amount  # Money earned also increases score

    def lose_life(self):
        """Decrease lives by 1. Check for game over."""
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def add_kill(self):
        """Increment kill count and award money."""
        self.kills += 1
        self.add_money(ENEMY_KILL_REWARD)

    def start_wave(self, wave_number: int, enemy_count: int):
        """
        Start a new wave.

        Args:
            wave_number: Wave number (1-indexed)
            enemy_count: Number of enemies in this wave
        """
        self.current_wave = wave_number
        self.wave_active = True
        self.enemies_in_wave = enemy_count
        self.enemies_spawned = 0

    def enemy_spawned(self):
        """Mark that an enemy has been spawned."""
        self.enemies_spawned += 1

    def wave_complete(self):
        """Mark current wave as complete."""
        self.wave_active = False
        # Award bonus for completing wave
        wave_bonus = self.current_wave * 50
        self.add_money(wave_bonus)

    def toggle_pause(self):
        """Toggle pause state."""
        self.paused = not self.paused

    def set_pause(self, paused: bool):
        """Set pause state."""
        self.paused = paused

    def is_paused(self) -> bool:
        """Check if game is paused."""
        return self.paused

    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.game_over

    def is_game_won(self) -> bool:
        """Check if player has won."""
        return self.game_won

    def reset(self):
        """Reset game state to initial values."""
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.score = 0
        self.kills = 0
        self.current_wave = 0
        self.wave_active = False
        self.enemies_in_wave = 0
        self.enemies_spawned = 0
        self.game_over = False
        self.game_won = False
        self.paused = False

    def get_stats(self) -> dict:
        """Get current game statistics."""
        return {
            'money': self.money,
            'lives': self.lives,
            'score': self.score,
            'kills': self.kills,
            'wave': self.current_wave,
            'wave_active': self.wave_active,
            'game_over': self.game_over,
            'game_won': self.game_won
        }

    def get_ui_info(self) -> dict:
        """Get information for UI display."""
        return {
            'money': f"${self.money}",
            'lives': f"Lives: {self.lives}",
            'wave': f"Wave: {self.current_wave}",
            'kills': f"Kills: {self.kills}",
            'score': f"Score: {self.score}"
        }
