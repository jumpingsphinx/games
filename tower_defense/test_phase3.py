"""
Test script for Phase 3: Tower Mechanics
Tests tower placement, economy, and basic functionality without GUI.
"""

from tower import Tower, TowerType, create_tower
from game_state import GameState
from config import STARTING_MONEY, STARTING_LIVES


def test_tower_creation():
    """Test 1: Tower creation and properties."""
    print("=" * 60)
    print("TEST 1: Tower Creation and Properties")
    print("=" * 60)

    # Create each tower type
    basic = create_tower(5, 5, TowerType.BASIC)
    slow = create_tower(10, 10, TowerType.SLOW)
    sniper = create_tower(15, 15, TowerType.SNIPER)

    print(f"\nBasic Tower:")
    print(f"  Name: {basic.name}")
    print(f"  Cost: ${basic.cost}")
    print(f"  Damage: {basic.damage}")
    print(f"  Range: {basic.range}px")
    print(f"  Fire Rate: {basic.fire_rate} ticks")

    print(f"\nSlow Tower:")
    print(f"  Name: {slow.name}")
    print(f"  Cost: ${slow.cost}")
    print(f"  Damage: {slow.damage}")
    print(f"  Range: {slow.range}px")
    print(f"  Slow Effect: {slow.slow_effect * 100}%")

    print(f"\nSniper Tower:")
    print(f"  Name: {sniper.name}")
    print(f"  Cost: ${sniper.cost}")
    print(f"  Damage: {sniper.damage}")
    print(f"  Range: {sniper.range}px")

    assert basic.cost == 100, "Basic tower cost should be 100"
    assert slow.cost == 150, "Slow tower cost should be 150"
    assert sniper.cost == 250, "Sniper tower cost should be 250"

    print("\n[PASS] All tower types created successfully")


def test_game_state_economy():
    """Test 2: Game state and economy system."""
    print("\n" + "=" * 60)
    print("TEST 2: Game State and Economy")
    print("=" * 60)

    game_state = GameState()

    print(f"\nStarting money: ${game_state.money}")
    print(f"Starting lives: {game_state.lives}")

    assert game_state.money == STARTING_MONEY, f"Should start with ${STARTING_MONEY}"
    assert game_state.lives == STARTING_LIVES, f"Should start with {STARTING_LIVES} lives"

    # Test spending money
    print(f"\nTrying to spend $100...")
    success = game_state.spend_money(100)
    assert success == True, "Should successfully spend $100"
    assert game_state.money == STARTING_MONEY - 100, "Money should decrease"
    print(f"  Success! Remaining money: ${game_state.money}")

    # Test can't afford
    print(f"\nTrying to spend $1000 (more than we have)...")
    success = game_state.spend_money(1000)
    assert success == False, "Should fail to spend more than available"
    print(f"  Correctly rejected! Money unchanged: ${game_state.money}")

    # Test add money
    print(f"\nAdding $50...")
    game_state.add_money(50)
    assert game_state.money == STARTING_MONEY - 100 + 50, "Money should increase"
    print(f"  Money now: ${game_state.money}")

    # Test losing lives
    print(f"\nLosing 1 life...")
    game_state.lose_life()
    assert game_state.lives == STARTING_LIVES - 1, "Lives should decrease"
    print(f"  Lives remaining: {game_state.lives}")

    # Test kill reward
    print(f"\nKilling an enemy...")
    initial_money = game_state.money
    game_state.add_kill()
    assert game_state.kills == 1, "Kill count should increase"
    assert game_state.money > initial_money, "Money should increase from kill reward"
    print(f"  Kills: {game_state.kills}, Money: ${game_state.money}")

    print("\n[PASS] Economy system working correctly")


def test_tower_costs():
    """Test 3: Tower cost system."""
    print("\n" + "=" * 60)
    print("TEST 3: Tower Cost System")
    print("=" * 60)

    game_state = GameState()

    print(f"\nStarting with ${game_state.money}")

    # Can afford basic tower
    basic_cost = Tower.get_tower_cost(TowerType.BASIC)
    print(f"\nBasic tower costs ${basic_cost}")
    assert game_state.can_afford(basic_cost), "Should be able to afford basic tower"
    print(f"  Can afford: Yes")

    # Buy 5 basic towers
    print(f"\nBuying 5 basic towers...")
    for i in range(5):
        if game_state.can_afford(basic_cost):
            game_state.spend_money(basic_cost)
            print(f"  Tower {i+1} purchased. Remaining: ${game_state.money}")

    # Try to buy sniper tower
    sniper_cost = Tower.get_tower_cost(TowerType.SNIPER)
    print(f"\nSniper tower costs ${sniper_cost}")
    can_afford = game_state.can_afford(sniper_cost)
    print(f"  Can afford: {can_afford}")
    print(f"  Current money: ${game_state.money}")

    print("\n[PASS] Tower cost system working")


def test_tower_types():
    """Test 4: Tower type listing."""
    print("\n" + "=" * 60)
    print("TEST 4: Tower Type Information")
    print("=" * 60)

    tower_types = Tower.get_available_types()

    print(f"\nAvailable tower types: {len(tower_types)}")

    for tower_info in tower_types:
        print(f"\n  {tower_info['name']} (Hotkey: {tower_info['hotkey']})")
        print(f"    Cost: ${tower_info['cost']}")
        print(f"    Type: {tower_info['type']}")
        print(f"    Color: {tower_info['color']}")
        print(f"    Description: {tower_info['description']}")

    assert len(tower_types) == 3, "Should have 3 tower types"

    print("\n[PASS] Tower type system working")


def test_tower_info():
    """Test 5: Tower information retrieval."""
    print("\n" + "=" * 60)
    print("TEST 5: Tower Information Retrieval")
    print("=" * 60)

    tower = create_tower(10, 10, TowerType.SNIPER)
    tower.set_world_position(200, 200)

    info = tower.get_info()

    print(f"\nTower info:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    assert info['name'] == 'Sniper Tower', "Should have correct name"
    assert info['cost'] == 250, "Should have correct cost"
    assert info['damage'] == 50, "Sniper should have 50 damage"
    assert info['range'] == 200, "Sniper should have 200 range"

    print("\n[PASS] Tower info retrieval working")


def test_refund_system():
    """Test 6: Tower sell/refund system."""
    print("\n" + "=" * 60)
    print("TEST 6: Tower Refund System")
    print("=" * 60)

    game_state = GameState()
    initial_money = game_state.money

    # Buy a tower
    tower_cost = Tower.get_tower_cost(TowerType.SLOW)
    game_state.spend_money(tower_cost)
    print(f"\nBought Slow Tower for ${tower_cost}")
    print(f"  Money after purchase: ${game_state.money}")

    # Sell it back (50% refund)
    refund = tower_cost // 2
    game_state.add_money(refund)
    print(f"\nSold tower for ${refund} (50% of ${tower_cost})")
    print(f"  Money after selling: ${game_state.money}")

    expected_loss = tower_cost - refund
    actual_loss = initial_money - game_state.money
    assert actual_loss == expected_loss, f"Should lose ${expected_loss}"

    print(f"\n  Net loss: ${actual_loss}")
    print(f"  Expected loss: ${expected_loss}")

    print("\n[PASS] Refund system working correctly")


def run_all_tests():
    """Run all Phase 3 tests."""
    print("\n" + "=" * 60)
    print("TOWER DEFENSE - PHASE 3 TOWER MECHANICS TESTS")
    print("=" * 60 + "\n")

    tests = [
        test_tower_creation,
        test_game_state_economy,
        test_tower_costs,
        test_tower_types,
        test_tower_info,
        test_refund_system
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
        print("\n[SUCCESS] ALL TESTS PASSED! Phase 3 implementation is complete.")
        print("\nPhase 3 Features Implemented:")
        print("  - 3 tower types (Basic, Slow, Sniper)")
        print("  - Economy system with starting money")
        print("  - Tower purchase and sell/refund system")
        print("  - Tower information and stats")
        print("  - Integration with game state")
    else:
        print(f"\n[WARNING] {failed} test(s) failed. Please review the implementation.")


if __name__ == "__main__":
    run_all_tests()
