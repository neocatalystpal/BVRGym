# 🚀 BVRGym Training Quick Start Guide

## Step 1: Setup Virtual Environment (ONE TIME ONLY)

```bash
cd /home/neosoft/Documents/BVRGym
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install gymnasium jsbsim pymap3d pandas py_trees stable_baselines3 tensorboard torch
```

## Step 2: Verify Setup Works

```bash
cd /home/neosoft/Documents/BVRGym
source venv/bin/activate
python3 test_setup.py
```

You should see:
```
============================================================
✓ ALL TESTS PASSED - Setup is working correctly!
============================================================
```

## Step 3: Start Training

```bash
cd /home/neosoft/Documents/BVRGym
source venv/bin/activate
python3 main.py
```

You should see output like:
```
Using cpu device
Logging to runs/PPO_X
-------- Model has been created --------
Total timesteps: 5,000,000
Logging to runs/PPO_X
| rollout/               |     |
| rollout/ep_len_mean    | 600 |
| rollout/ep_rew_mean    | -XX |
...
```

## Step 4: Monitor Training Progress (NEW TERMINAL)

```bash
cd /home/neosoft/Documents/BVRGym
source venv/bin/activate
tensorboard --logdir=runs
```

Then open browser: **http://localhost:6006**

## 📊 What to Look For in TensorBoard

1. **ep_len_mean** - Should stabilize around 600s (your episode length)
2. **ep_rew_mean** - Should increase over time (agent learning better rewards)
3. **policy_loss** - Should decrease over time (better policy)
4. **value_loss** - Should decrease over time (better value estimation)

## ✅ Verification Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (no import errors)
- [ ] test_setup.py runs without errors
- [ ] main.py starts training without crashes
- [ ] TensorBoard shows training metrics
- [ ] rewards are increasing (not stuck at -1000)

## 🐛 Troubleshooting

**Problem:** ModuleNotFoundError when running python3 main.py
**Solution:** Make sure you activated virtual environment: `source venv/bin/activate`

**Problem:** JSBSim errors
**Solution:** JSBSim is a heavy simulator. First training run may take time to initialize.

**Problem:** Out of memory
**Solution:** Reduce n_envs from 32 to 16 or 8 in main.py

**Problem:** TensorBoard shows no data
**Solution:** Make sure main.py is still running. Training generates logs as it progresses.

## 📈 Key Improvements Made

✓ Enhanced reward function with 6 tactical bonuses
✓ Training increased from 2M to 5M timesteps  
✓ Parallel environments increased from 14 to 32
✓ Red agent now launches missiles tactically
✓ Behavior tree improved with dynamic tactics
✓ Episode length increased from 10 to 30 minutes
✓ Missile tracking fixed in observations

## 🎯 Expected Results

After ~500K steps:
- Agent should learn to move toward enemy
- Should launch missiles in proper range
- Rewards should increase noticeably

After ~2M steps:
- Agent should develop tactical maneuvers
- Win rate against red agent should improve
- Missile launches should be strategic

## 💾 Saved Models

Your trained models will be saved to:
```
trained/BVRBase_PPO_5M_improved
```

---

**Need more help? Check the main README.md for advanced topics!**
