"""
Test script for Phase 4: Enemy Mechanics
Tests enemy creation, movement, and wave system without GUI.
"""

from enemy import Enemy, EnemyType, EnemySpawner, create_enemy
from config import BASE_ENEMY_HEALTH, BASE_ENEMY_SPEED


def test_enemy_creation():
    """Test 1: Enemy creation and properties."""
    print("=" * 60)
    print("TEST 1: Enemy Creation and Properties")
    print("=" * 60)

    path = [(0, 0), (5, 0), (5, 5), (10, 5)]

    # Create each enemy type
    basic = create_enemy(path, EnemyType.BASIC, wave_number=1)
    fast = create_enemy(path, EnemyType.FAST, wave_number=1)
    tank = create_enemy(path, EnemyType.TANK, wave_number=1)

    print(f"\nBasic Enemy:")
    print(f"  Name: {basic.name}")
    print(f"  Health: {basic.max_health}")
    print(f"  Speed: {basic.base_speed}")
    print(f"  Reward: ${basic.reward}")

    print(f"\nFast Enemy:")
    print(f"  Name: {fast.name}")
    print(f"  Health: {fast.max_health}")
    print(f"  Speed: {fast.base_speed}")
    print(f"  Reward: ${fast.reward}")

    print(f"\nTank Enemy:")
    print(f"  Name: {tank.name}")
    print(f"  Health: {tank.max_health}")
    print(f"  Speed: {tank.base_speed}")
    print(f"  Reward: ${tank.reward}")

    assert basic.is_alive(), "Enemy should start alive"
    assert not basic.has_reached_end(), "Enemy should not have reached end"
    assert basic.max_health == BASE_ENEMY_HEALTH, "Basic enemy should have base health"

    print("\n[PASS] All enemy types created successfully")


def test_enemy_damage():
    """Test 2: Enemy damage and death."""
    print("\n" + "=" * 60)
    print("TEST 2: Enemy Damage and Death")
    print("=" * 60)

    path = [(0, 0), (5, 0)]
    enemy = create_enemy(path, EnemyType.BASIC, wave_number=1)

    initial_health = enemy.health
    print(f"\nInitial health: {initial_health}")

    # Apply damage
    enemy.take_damage(20)
    print(f"After 20 damage: {enemy.health}")
    assert enemy.health == initial_health - 20, "Health should decrease"
    assert enemy.is_alive(), "Enemy should still be alive"

    # Kill enemy
    enemy.take_damage(1000)
    print(f"After 1000 damage: {enemy.health}")
    assert enemy.health == 0, "Health should be 0"
    assert not enemy.is_alive(), "Enemy should be dead"

    print("\n[PASS] Enemy damage system working")


def test_enemy_slow():
    """Test 3: Enemy slow effect."""
    print("\n" + "=" * 60)
    print("TEST 3: Enemy Slow Effect")
    print("=" * 60)

    path = [(0, 0), (5, 0)]
    enemy = create_enemy(path, EnemyType.BASIC, wave_number=1)

    print(f"\nNormal speed multiplier: {enemy.slow_multiplier}")
    assert enemy.slow_multiplier == 1.0, "Should start at normal speed"

    # Apply slow
    enemy.apply_slow(0.5, 60)  # 50% speed for 60 ticks
    print(f"After applying slow: {enemy.slow_multiplier}")
    print(f"Slow duration: {enemy.slow_duration} ticks")

    assert enemy.slow_multiplier == 0.5, "Should be slowed to 50%"
    assert enemy.slow_duration == 60, "Should have 60 ticks duration"

    # Update to reduce slow duration
    for i in range(60):
        enemy.update(dt=1.0)

    print(f"After 60 updates: {enemy.slow_multiplier}")
    assert enemy.slow_multiplier == 1.0, "Slow should wear off"

    print("\n[PASS] Slow effect system working")


def test_wave_generation():
    """Test 4: Wave generation."""
    print("\n" + "=" * 60)
    print("TEST 4: Wave Generation")
    print("=" * 60)

    path = [(0, 0), (5, 0), (10, 0)]
    spawner = EnemySpawner(path)

    # Wave 1 (should be only basic enemies)
    spawner.start_wave(1)
    wave1_count = spawner.get_remaining_count()
    print(f"\nWave 1 enemy count: {wave1_count}")
    assert wave1_count > 0, "Wave should have enemies"

    # Wave 5 (should have mixed enemies)
    spawner2 = EnemySpawner(path)
    spawner2.start_wave(5)
    wave5_count = spawner2.get_remaining_count()
    print(f"Wave 5 enemy count: {wave5_count}")
    assert wave5_count > wave1_count, "Later waves should have more enemies"

    # Wave 10 (should have all enemy types)
    spawner3 = EnemySpawner(path)
    spawner3.start_wave(10)
    wave10_count = spawner3.get_remaining_count()
    print(f"Wave 10 enemy count: {wave10_count}")
    assert wave10_count > wave5_count, "Wave 10 should have even more enemies"

    print("\n[PASS] Wave generation working")


def test_enemy_spawning():
    """Test 5: Enemy spawning system."""
    print("\n" + "=" * 60)
    print("TEST 5: Enemy Spawning System")
    print("=" * 60)

    path = [(0, 0), (5, 0), (10, 0)]
    spawner = EnemySpawner(path)

    spawner.start_wave(1)
    initial_count = spawner.get_remaining_count()
    print(f"\nEnemies to spawn: {initial_count}")

    # Spawn first enemy (need to update multiple times due to spawn interval)
    spawned_count = 0
    for i in range(1000):  # Update enough times to spawn all (30 ticks between spawns)
        enemy = spawner.update(dt=1.0)
        if enemy:
            spawned_count += 1
            assert enemy.is_alive(), "Spawned enemy should be alive"

    print(f"Enemies spawned: {spawned_count}")
    assert spawned_count == initial_count, f"Should spawn all {initial_count} enemies"
    assert spawner.is_wave_complete(), "Wave should be complete"

    print("\n[PASS] Enemy spawning working")


def test_enemy_movement():
    """Test 6: Enemy path following."""
    print("\n" + "=" * 60)
    print("TEST 6: Enemy Path Following")
    print("=" * 60)

    # Simple straight path
    path = [(0, 0), (5, 0)]
    enemy = create_enemy(path, EnemyType.BASIC, wave_number=1)

    print(f"\nStarting position: ({enemy.x:.1f}, {enemy.y:.1f})")
    print(f"Path index: {enemy.path_index}")

    # Update enemy many times
    for i in range(500):
        enemy.update(dt=1.0)
        if enemy.has_reached_end():
            break

    print(f"Final position: ({enemy.x:.1f}, {enemy.y:.1f})")
    print(f"Reached end: {enemy.has_reached_end()}")
    print(f"Updates needed: {i+1}")

    assert enemy.has_reached_end(), "Enemy should reach end of path"
    assert enemy.is_alive(), "Enemy should still be alive"

    print("\n[PASS] Enemy movement working")


def test_wave_scaling():
    """Test 7: Wave difficulty scaling."""
    print("\n" + "=" * 60)
    print("TEST 7: Wave Difficulty Scaling")
    print("=" * 60)

    path = [(0, 0), (5, 0)]

    # Wave 1 enemy
    wave1_enemy = create_enemy(path, EnemyType.BASIC, wave_number=1)

    # Wave 5 enemy
    wave5_enemy = create_enemy(path, EnemyType.BASIC, wave_number=5)

    print(f"\nWave 1 Basic Enemy:")
    print(f"  Health: {wave1_enemy.max_health:.1f}")
    print(f"  Speed: {wave1_enemy.base_speed:.2f}")

    print(f"\nWave 5 Basic Enemy:")
    print(f"  Health: {wave5_enemy.max_health:.1f}")
    print(f"  Speed: {wave5_enemy.base_speed:.2f}")

    assert wave5_enemy.max_health > wave1_enemy.max_health, "Later waves should have more health"
    assert wave5_enemy.base_speed > wave1_enemy.base_speed, "Later waves should be faster"

    print(f"\nHealth increase: {(wave5_enemy.max_health / wave1_enemy.max_health - 1) * 100:.1f}%")
    print(f"Speed increase: {(wave5_enemy.base_speed / wave1_enemy.base_speed - 1) * 100:.1f}%")

    print("\n[PASS] Wave scaling working")


def run_all_tests():
    """Run all Phase 4 tests."""
    print("\n" + "=" * 60)
    print("TOWER DEFENSE - PHASE 4 ENEMY MECHANICS TESTS")
    print("=" * 60 + "\n")

    tests = [
        test_enemy_creation,
        test_enemy_damage,
        test_enemy_slow,
        test_wave_generation,
        test_enemy_spawning,
        test_enemy_movement,
        test_wave_scaling
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
        print("\n[SUCCESS] ALL TESTS PASSED! Phase 4 implementation is complete.")
        print("\nPhase 4 Features Implemented:")
        print("  - 3 enemy types (Basic, Fast, Tank)")
        print("  - Enemy health and damage system")
        print("  - Enemy slow effects")
        print("  - Wave generation with scaling difficulty")
        print("  - Enemy spawning system")
        print("  - Path following movement")
        print("  - Integration with game state")
    else:
        print(f"\n[WARNING] {failed} test(s) failed. Please review the implementation.")


if __name__ == "__main__":
    run_all_tests()
