# ✅ Complete Verification & Testing Guide

## What I Did - Summary

I've made **5 major improvements** to your BVRGym AI training system:

1. ✅ **Enhanced Reward Function** - 6 tactical bonuses instead of simple +1/-1
2. ✅ **Better Training Config** - 5M steps, 32 parallel envs, optimized hyperparameters
3. ✅ **Fixed Missile Tracking** - AI now sees when missiles are active
4. ✅ **Red Agent Improvements** - Now launches missiles and adapts tactics
5. ✅ **Extended Episodes** - 30 minutes instead of 10 for complex strategies

---

## How to Verify Everything Works

### STEP 1: Quick Verification (2 minutes)

```bash
# Open a terminal and run:
cd /home/neosoft/Documents/BVRGym
bash setup.sh
```

This will:
- ✓ Check Python installation
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Verify code syntax
- ✓ Run quick test

**Expected output:** `✓ SETUP COMPLETE - Ready to start training!`

---

### STEP 2: Check All Files Manually

```bash
# Make sure these files were updated:
grep -l "distance_reward\|alt_diff\|mach_diff" jsb_gym/envs/BaseEnv.py
# Should show: jsb_gym/envs/BaseEnv.py

grep -l "n_envs = 32\|total_timesteps = 5_000_000" main.py
# Should show: main.py

grep -l "max_episode_time = 60\*30" jsb_gym/envs/config/baseEnv_conf.py
# Should show: jsb_gym/envs/config/baseEnv_conf.py

grep -l "dynamic" jsb_gym/bts/bts.py
# Should show: jsb_gym/bts/bts.py
```

All should return the file names.

---

### STEP 3: Start Training

```bash
# Make sure virtual env is activated:
source venv/bin/activate

# Start training (this will run for HOURS)
python3 main.py
```

**Watch for:**
- ✅ NO ImportError
- ✅ NO "ModuleNotFoundError"
- ✅ Training starts with timesteps count
- ✅ Output shows: `| rollout/ep_rew_mean |`

**Example good output:**
```
Using cpu device
Logging to runs/PPO_X
-------- Model has been created --------
Total timesteps: 5,000,000

| rollout/               |     |
| rollout/ep_len_mean    | 600 |
| rollout/ep_rew_mean    | -XX |
```

---

### STEP 4: Monitor with TensorBoard (NEW TERMINAL)

While training is running, open another terminal:

```bash
cd /home/neosoft/Documents/BVRGym
source venv/bin/activate
tensorboard --logdir=runs
```

Then open in browser: **http://localhost:6006**

**Key metrics to watch:**

| Metric | What to Look For |
|--------|------------------|
| `ep_rew_mean` | Should increase over time (not stuck at -1000) |
| `ep_len_mean` | Should be around 1800 seconds |
| `policy_loss` | Should trend downward |
| `value_loss` | Should trend downward |
| `fps` | Higher is better (training speed) |

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'gymnasium'`

**Solution:**
```bash
# Activate virtual environment first:
source venv/bin/activate

# Then run main.py:
python3 main.py
```

---

### Issue: `PermissionError` when creating venv

**Solution:**
```bash
chmod +x setup.sh
bash setup.sh
```

---

### Issue: `Out of memory` error

**Solution:** Reduce parallel environments in `main.py`:

Change:
```python
n_envs = 32  # Current
```

To:
```python
n_envs = 16  # or 8
```

---

### Issue: Training is too slow

**Solution:** Check if using GPU. In TensorBoard, look for `device`. If it says `cpu`, consider:
- Install CUDA: https://docs.nvidia.com/cuda/
- Or reduce n_envs to speed up overall training

---

## What to Expect During Training

### First 10 minutes:
- Initialization messages
- First episode running
- Rewards likely negative (-1000 range)

### After 100K steps (~1-2 hours):
- Reward should start improving slightly
- Agent learning basic movement
- TensorBoard shows first meaningful data

### After 500K steps (~5-10 hours):
- Clear improvement in rewards
- Agent launching missiles
- Win rate should increase

### After 2M steps (~20-30 hours):
- Agent develops tactical behavior
- Significant reward improvement
- Should see convergence patterns

### Final (5M steps, ~50-100 hours):
- Fully trained model
- Saved to: `trained/BVRBase_PPO_5M_improved`

---

## Files You Can Check

### Verification Test Script
```bash
python3 test_setup.py
```
Tells you:
- ✓ Environment imports correctly
- ✓ Configuration is valid
- ✓ Agents created successfully
- ✓ Reward function has all improvements

### Quick Reference
- `QUICK_START.md` - Fast reference guide
- `IMPROVEMENTS_SUMMARY.md` - Detailed change log
- `setup.sh` - Automated setup script

---

## Running Training in Background

If you want to close the terminal and let training continue:

```bash
# Start training in background:
nohup python3 main.py > training.log 2>&1 &

# Check progress:
tail -f training.log

# Check if still running:
ps aux | grep "main.py"

# Stop training:
pkill -f "main.py"
```

---

## Summary Checklist

Before you start, verify:
- [ ] Python 3.11+ installed
- [ ] Virtual environment created (`venv` folder exists)
- [ ] Dependencies installed (run `pip list` to check)
- [ ] No syntax errors (run `python3 -m py_compile main.py`)
- [ ] Test runs successfully (`python3 test_setup.py`)

When training starts, verify:
- [ ] No ImportError in console
- [ ] Training timesteps incrementing
- [ ] Output shows reward values
- [ ] TensorBoard shows metrics
- [ ] Reward trending upward after 500K steps

---

## 🎯 Success Indicators

✅ **Training is working if:**
- No crashes after 1 hour
- Rewards show any improvement
- TensorBoard displays metrics
- No "out of memory" errors

✅ **Training is improving if:**
- After 500K steps: Rewards > -500
- After 2M steps: Rewards > -100
- After 5M steps: Rewards > 0

✅ **Model is ready when:**
- Total timesteps: 5,000,000 complete
- Model saved to: `trained/BVRBase_PPO_5M_improved`
- Rewards stabilized at positive values

---

**You're all set! Start with `bash setup.sh` and then `python3 main.py`** 🚀
