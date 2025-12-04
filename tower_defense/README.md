# Tower Defense Game - Dynamic Pathfinding

A tower defense game built with Python and Pygame featuring real-time A* pathfinding that dynamically adapts to tower placement.

## Current Status: Phase 2 Complete ✅

**Completed Phases:**
- ✅ Phase 1: Foundation (Grid, Window, Mouse Interaction)
- ✅ Phase 2: Pathfinding (A* Algorithm, Path Visualization, Blocking Prevention)

**Upcoming Phases:**
- ⏳ Phase 3: Tower Mechanics
- ⏳ Phase 4: Enemy Mechanics
- ⏳ Phase 5: Game Logic
- ⏳ Phase 6: Polish & UI

## Features

### Phase 1: Foundation
- 40x30 grid system with 20px tiles (800x600 window)
- Mouse interaction for tower placement
- Grid coordinate conversion
- Debug mode with grid coordinates
- Hover highlighting for valid/invalid placements

### Phase 2: Pathfinding ⭐ NEW
- **A* Pathfinding Algorithm** - Optimal path finding from start to end
- **Dynamic Path Recalculation** - Path updates when towers are placed/removed
- **Path Blocking Prevention** - Cannot place towers that completely block the path
- **Real-time Path Visualization** - See the path enemies will follow
- **Comprehensive Test Suite** - 7 tests covering all pathfinding scenarios

## Installation

### Prerequisites
```bash
Python 3.10 or higher
Pygame library
```

### Install Dependencies
```bash
pip install pygame
```

## Running the Game

### Start the Game
```bash
cd tower_defense
python main.py
```

### Run Tests
```bash
python test_phase2.py
```

### Test Pathfinding Module Directly
```bash
python pathfinding.py
```

## Controls

### Mouse Controls
- **Left Click** - Place or remove a tower
- **Right Click** - Remove a tower

### Keyboard Controls
| Key | Action |
|-----|--------|
| `P` | Pause/Resume game |
| `D` | Toggle debug information |
| `V` | Toggle path visualization ⭐ NEW |
| `R` | Reset grid (clears towers, keeps start/end) |
| `ESC` | Quit game |

## How to Play (Current Phase)

1. **Start the game** - You'll see a grid with a green START point on the left and red END point on the right
2. **View the path** - A yellow line shows the current path from start to end
3. **Place towers** - Left-click on empty cells to place towers (blue)
   - Valid placement locations show a green highlight
   - Invalid locations (would block path) show a red highlight
4. **Watch path adapt** - The yellow path dynamically recalculates around your towers
5. **Experiment** - Try to create mazes and see how the pathfinding adapts!

## Game Rules

- You **cannot** place towers on the start or end points
- You **cannot** completely block the path from start to end
- The pathfinding algorithm always finds the shortest valid path
- Towers are shown in blue, the path in yellow

## Visual Guide

```
Legend:
🟢 Green Cell  - Start point (enemies spawn here)
🔴 Red Cell    - End point (enemies try to reach here)
🔵 Blue Cell   - Tower (blocks enemy movement)
🟡 Yellow Line - Current path enemies will follow
⬜ White Border - Valid tower placement
🟥 Red Border  - Invalid tower placement
```

## Project Structure

```
tower_defense/
├── main.py              # Entry point and game loop
├── config.py            # Constants and configuration
├── grid.py              # Grid system with pathfinding integration
├── pathfinding.py       # A* pathfinding implementation
├── utils.py             # Helper functions
├── test_phase2.py       # Comprehensive test suite
├── PHASE2_SUMMARY.md    # Detailed Phase 2 documentation
└── README.md            # This file
```

## Technical Details

### Grid System
- **Size**: 40 columns × 30 rows
- **Tile Size**: 20×20 pixels
- **Total Window**: 800×600 pixels
- **Grid States**: Empty, Tower, Wall, Start, End

### Pathfinding
- **Algorithm**: A* with Manhattan distance heuristic
- **Movement**: Cardinal directions only (no diagonal)
- **Optimization**: Path is cached and only recalculated on grid changes
- **Validation**: Placement is tested before allowing tower placement

### Performance
- **Frame Rate**: Capped at 60 FPS
- **Pathfinding**: Typically < 1ms for 40×30 grid
- **Memory**: Minimal - only current path stored

## Development Roadmap

### Phase 3: Tower Mechanics
- [ ] Tower placement cost system
- [ ] Basic shooting tower
- [ ] Projectile system with collision detection
- [ ] Multiple tower types (basic, slow, sniper)
- [ ] Range visualization

### Phase 4: Enemy Mechanics
- [ ] Enemy spawning system
- [ ] Path following behavior
- [ ] Health and damage system
- [ ] Multiple enemy types
- [ ] Wave system

### Phase 5: Game Logic
- [ ] Resource management (money)
- [ ] Life system
- [ ] Wave progression
- [ ] Win/lose conditions
- [ ] Score tracking

### Phase 6: Polish & UI
- [ ] Start menu
- [ ] Game over screen
- [ ] UI overlay (money, lives, waves)
- [ ] Tower selection menu
- [ ] Sound effects (optional)

## Testing

The project includes comprehensive tests for Phase 2:

```bash
python test_phase2.py
```

**Test Coverage:**
1. Basic pathfinding with no obstacles
2. Pathfinding around obstacles
3. Complex maze navigation
4. Blocked path detection
5. Tower placement validation
6. Dynamic path recalculation
7. Edge cases (start==end, adjacent positions)

All tests pass successfully! ✅

## Configuration

Edit [config.py](config.py) to customize:

```python
# Grid settings
TILE_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 30

# Start and end positions
DEFAULT_START = (2, 15)
DEFAULT_END = (37, 15)

# Colors
COLORS = {
    'path': (255, 200, 50),  # Yellow path
    'tower': (100, 100, 180), # Blue towers
    # ... and more
}
```

## Troubleshooting

### Game won't start
- Make sure Pygame is installed: `pip install pygame`
- Check Python version: `python --version` (need 3.10+)

### Can't place towers
- Red highlight means placement would block the path
- Can't place on start/end points (green/red cells)
- Try placing towers that leave a gap for the path

### Path looks wrong
- Path always shows the shortest valid route
- Try toggling path visualization with `V` key
- Check debug mode with `D` key to see path status

## Credits

**Development Phase**: Phase 2 - Pathfinding System
**Python Version**: 3.10+
**Libraries**: Pygame
**Algorithm**: A* Pathfinding with Manhattan Distance Heuristic

## License

Educational project - free to use and modify.

## Next Steps

To continue development:
1. Review [PHASE2_SUMMARY.md](PHASE2_SUMMARY.md) for technical details
2. Start implementing Phase 3: Tower Mechanics
3. Follow the roadmap in the original specification

---

**Enjoy the dynamic pathfinding!** 🎮
Try creating complex mazes and watch the path intelligently navigate around your towers.
