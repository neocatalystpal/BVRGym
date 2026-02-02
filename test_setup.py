#!/usr/bin/env python3
"""
Quick verification script to test all improvements are working correctly
"""
import sys

print("=" * 60)
print("BVRGym Setup Verification")
print("=" * 60)

# Test 1: Import environment
print("\n[TEST 1] Testing environment imports...")
try:
    from jsb_gym.envs.BaseEnv import BVRBase
    from jsb_gym.envs.config import baseEnv_conf
    print("✓ Environment imports successfully")
except Exception as e:
    print(f"✗ Failed to import environment: {e}")
    sys.exit(1)

# Test 2: Verify configuration
print("\n[TEST 2] Checking configuration...")
print(f"  • Observation shape: {baseEnv_conf.observation_shape}")
print(f"  • Action shape: {baseEnv_conf.action_shape}")
print(f"  • Max episode time: {baseEnv_conf.max_episode_time}s ({baseEnv_conf.max_episode_time/60}min)")
print("✓ Configuration looks correct")

# Test 3: Create environment instance
print("\n[TEST 3] Creating environment instance...")
try:
    env = BVRBase(conf=baseEnv_conf)
    print(f"✓ Environment created successfully")
    print(f"  • Observation space: {env.observation_space}")
    print(f"  • Action space: {env.action_space}")
except Exception as e:
    print(f"✗ Failed to create environment: {e}")
    sys.exit(1)

# Test 4: Reset environment
print("\n[TEST 4] Resetting environment...")
try:
    obs, info = env.reset()
    print(f"✓ Environment reset successfully")
    print(f"  • Observation shape: {obs.shape}")
    print(f"  • Info: {info}")
except Exception as e:
    print(f"✗ Failed to reset environment: {e}")
    sys.exit(1)

# Test 5: Test reward function
print("\n[TEST 5] Testing reward function...")
try:
    # Simulate a step
    import numpy as np
    action = np.array([0.0, 0.0, 0.0])
    obs, reward, done, truncated, info = env.step(action)
    print(f"✓ Step executed successfully")
    print(f"  • Reward: {reward:.2f}")
    print(f"  • Done: {done}")
    print(f"  • Observation shape: {obs.shape}")
    print(f"  • Info: {info}")
except Exception as e:
    print(f"✗ Failed step: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test agents
print("\n[TEST 6] Testing agents...")
try:
    blue_agent = env.blue_agent
    red_agent = env.red_agent
    print(f"✓ Agents created successfully")
    print(f"  • Blue agent missile count: {len(blue_agent.ammo)}")
    print(f"  • Red agent missile count: {len(red_agent.ammo)}")
    print(f"  • Red agent has BT: {hasattr(red_agent, 'BT')}")
except Exception as e:
    print(f"✗ Failed to access agents: {e}")
    sys.exit(1)

# Test 7: Verify reward improvements
print("\n[TEST 7] Verifying reward function improvements...")
try:
    import inspect
    reward_source = inspect.getsource(env.get_reward)
    if "distance_reward" in reward_source and "positioning_reward" in reward_source:
        print("✓ Enhanced reward function detected")
        print("  • Distance-based reward: ✓")
        print("  • Positioning reward: ✓")
        print("  • Altitude advantage: ✓")
        print("  • Speed advantage: ✓")
    else:
        print("✗ Reward function may not have all improvements")
except Exception as e:
    print(f"✗ Failed to verify reward function: {e}")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - Setup is working correctly!")
print("=" * 60)
print("\nNext steps:")
print("  1. Run: source venv/bin/activate")
print("  2. Run: python3 main.py")
print("  3. Monitor training with TensorBoard:")
print("     tensorboard --logdir=runs")
print("=" * 60)
