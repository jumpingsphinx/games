# Tower Defense Game with Dynamic Pathfinding

A Python tower defense game featuring real-time pathfinding where enemy routes dynamically change based on tower placement.

## Current Status: Phase 1 Complete ✓

### Phase 1 - Foundation
- ✅ Pygame window and game loop
- ✅ Grid rendering (40x30 tiles, 20px each)
- ✅ Mouse interaction for grid selection
- ✅ Tower placement/removal
- ✅ Visual hover feedback (green = valid, red = invalid)
- ✅ Pause functionality
- ✅ Debug information display

## Installation

```bash
# Install dependencies
pip install pygame

# Run the game
python main.py
```

## Controls

| Key/Action | Description |
|------------|-------------|
| **Left Click** | Place or remove tower |
| **Right Click** | Remove tower |
| **P** | Pause/unpause game |
| **D** | Toggle debug info display |
| **R** | Reset grid to initial state |
| **ESC** | Quit game |

## Project Structure

```
tower_defense/
├── main.py          # Entry point and game loop
├── config.py        # Constants and configuration
├── grid.py          # Grid system and rendering
├── utils.py         # Helper functions
└── README.md        # This file
```

## Grid Legend

| Color | Meaning |
|-------|---------|
| 🟩 Green | Start point (enemy spawn) |
| 🟥 Red | End point (enemy destination) |
| 🟦 Blue | Tower |
| ⬛ Dark gray | Empty cell |

## Upcoming Phases

- **Phase 2**: A* Pathfinding implementation
- **Phase 3**: Tower mechanics (shooting, projectiles)
- **Phase 4**: Enemy mechanics (waves, health, variants)
- **Phase 5**: Game logic (economy, lives, scoring)
- **Phase 6**: Polish & UI (menus, effects)

## Configuration

Edit `config.py` to customize:
- Window size
- Grid dimensions
- Tile size
- Colors
- Start/end positions
