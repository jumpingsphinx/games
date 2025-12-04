"""
Test script for Phase 2: Pathfinding System
Tests all pathfinding features without requiring GUI.
"""

from pathfinding import Pathfinder
from config import EMPTY, TOWER, START, END


def print_grid(grid, path=None, start=None, end=None, title="Grid"):
    """Helper to visualize a grid."""
    width = len(grid)
    height = len(grid[0]) if width > 0 else 0

    print(f"\n{title}")
    print("S = Start, E = End, # = Tower, * = Path, . = Empty")
    print()

    for y in range(height):
        for x in range(width):
            if (x, y) == start:
                print("S", end=" ")
            elif (x, y) == end:
                print("E", end=" ")
            elif grid[x][y] == TOWER:
                print("#", end=" ")
            elif path and (x, y) in path:
                print("*", end=" ")
            else:
                print(".", end=" ")
        print()
    print()


def test_basic_pathfinding():
    """Test 1: Basic pathfinding with no obstacles."""
    print("=" * 60)
    print("TEST 1: Basic Pathfinding (No Obstacles)")
    print("=" * 60)

    width, height = 15, 10
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]
    start = (2, 5)
    end = (12, 5)

    pathfinder = Pathfinder(width, height)
    path = pathfinder.find_path(grid, start, end)

    print_grid(grid, path, start, end, "Direct path test")

    assert path is not None, "Path should exist!"
    assert len(path) == 11, f"Path length should be 11, got {len(path)}"
    print(f"[PASS] Path found with length {len(path)}")


def test_path_with_obstacles():
    """Test 2: Pathfinding around obstacles."""
    print("=" * 60)
    print("TEST 2: Pathfinding Around Obstacles")
    print("=" * 60)

    width, height = 15, 10
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]
    start = (2, 5)
    end = (12, 5)

    # Create a wall with a gap
    for y in range(2, 9):
        if y != 5:  # Leave gap
            grid[7][y] = TOWER

    pathfinder = Pathfinder(width, height)
    path = pathfinder.find_path(grid, start, end)

    print_grid(grid, path, start, end, "Path around wall")

    assert path is not None, "Path should exist through gap!"
    assert (7, 5) in path, "Path should go through the gap"
    print(f"[PASS] Path navigated around obstacle, length {len(path)}")


def test_complex_maze():
    """Test 3: Complex maze pathfinding."""
    print("=" * 60)
    print("TEST 3: Complex Maze Navigation")
    print("=" * 60)

    width, height = 15, 10
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]
    start = (1, 1)
    end = (13, 8)

    # Create a complex maze
    obstacles = [
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
        (10, 5), (10, 6), (10, 7), (10, 8), (10, 9),
        (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)
    ]

    for pos in obstacles:
        if 0 <= pos[0] < width and 0 <= pos[1] < height:
            grid[pos[0]][pos[1]] = TOWER

    pathfinder = Pathfinder(width, height)
    path = pathfinder.find_path(grid, start, end)

    print_grid(grid, path, start, end, "Maze navigation")

    assert path is not None, "Path should exist through maze!"
    print(f"[PASS] Successfully navigated maze, path length {len(path)}")


def test_blocked_path():
    """Test 4: Detecting completely blocked path."""
    print("=" * 60)
    print("TEST 4: Blocked Path Detection")
    print("=" * 60)

    width, height = 15, 10
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]
    start = (2, 5)
    end = (12, 5)

    # Create complete wall with no gap
    for y in range(height):
        grid[7][y] = TOWER

    pathfinder = Pathfinder(width, height)
    path = pathfinder.find_path(grid, start, end)

    print_grid(grid, path, start, end, "Completely blocked path")

    assert path is None, "Path should be None when completely blocked!"
    print("[PASS] Correctly detected blocked path")


def test_would_block_validation():
    """Test 5: Validate tower placement blocking."""
    print("=" * 60)
    print("TEST 5: Tower Placement Validation")
    print("=" * 60)

    width, height = 10, 7
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]
    start = (1, 3)
    end = (8, 3)

    # Create a narrow corridor
    for x in range(width):
        grid[x][2] = TOWER
        grid[x][4] = TOWER

    pathfinder = Pathfinder(width, height)

    # Test placing tower in the corridor
    test_pos = (5, 3)  # In the middle of the path
    would_block = pathfinder.would_block_path(grid, test_pos, start, end)

    print_grid(grid, None, start, end, "Narrow corridor")
    print(f"Testing placement at position {test_pos}")
    print(f"Would block: {would_block}")

    assert would_block == True, "Placing in corridor should block path!"
    print("[PASS] Correctly validated that placement would block path")

    # Test placing tower outside corridor
    test_pos2 = (5, 1)  # Above corridor
    would_block2 = pathfinder.would_block_path(grid, test_pos2, start, end)
    print(f"\nTesting placement at position {test_pos2}")
    print(f"Would block: {would_block2}")

    assert would_block2 == False, "Placing outside corridor should not block!"
    print("[PASS] Correctly validated safe tower placement")


def test_path_update_on_change():
    """Test 6: Path updates when grid changes."""
    print("=" * 60)
    print("TEST 6: Dynamic Path Recalculation")
    print("=" * 60)

    width, height = 12, 8
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]
    start = (1, 4)
    end = (10, 4)

    pathfinder = Pathfinder(width, height)

    # Initial path (straight)
    pathfinder.update_path(grid, start, end)
    initial_path = pathfinder.get_path()
    print_grid(grid, initial_path, start, end, "Initial straight path")
    print(f"Initial path length: {len(initial_path)}")

    # Add obstacle in the middle
    grid[6][4] = TOWER

    # Update path
    pathfinder.update_path(grid, start, end)
    new_path = pathfinder.get_path()
    print_grid(grid, new_path, start, end, "Path recalculated around new obstacle")
    print(f"New path length: {len(new_path)}")

    assert len(new_path) > len(initial_path), "Path should be longer after obstacle!"
    assert pathfinder.has_path(), "Path should still exist!"
    print("[PASS] Path successfully recalculated around new obstacle")


def test_edge_cases():
    """Test 7: Edge cases."""
    print("=" * 60)
    print("TEST 7: Edge Cases")
    print("=" * 60)

    # Test with start == goal
    width, height = 5, 5
    grid = [[EMPTY for _ in range(height)] for _ in range(width)]
    start = (2, 2)
    end = (2, 2)

    pathfinder = Pathfinder(width, height)
    path = pathfinder.find_path(grid, start, end)

    print(f"Start == End: Path = {path}")
    assert path is not None, "Should return path even when start == end"
    print("[PASS] Handled start == end case")

    # Test with adjacent positions
    start2 = (2, 2)
    end2 = (3, 2)
    path2 = pathfinder.find_path(grid, start2, end2)
    print(f"Adjacent positions: Path length = {len(path2)}")
    assert len(path2) == 2, "Adjacent positions should have path length 2"
    print("[PASS] Handled adjacent positions")


def run_all_tests():
    """Run all pathfinding tests."""
    print("\n" + "=" * 60)
    print("TOWER DEFENSE - PHASE 2 PATHFINDING TESTS")
    print("=" * 60 + "\n")

    tests = [
        test_basic_pathfinding,
        test_path_with_obstacles,
        test_complex_maze,
        test_blocked_path,
        test_would_block_validation,
        test_path_update_on_change,
        test_edge_cases
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
            print("[PASS] TEST PASSED\n")
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] TEST FAILED: {e}\n")
        except Exception as e:
            failed += 1
            print(f"[ERROR] TEST ERROR: {e}\n")

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)

    if failed == 0:
        print("\n[SUCCESS] ALL TESTS PASSED! Phase 2 implementation is complete.")
    else:
        print(f"\n[WARNING] {failed} test(s) failed. Please review the implementation.")


if __name__ == "__main__":
    run_all_tests()
