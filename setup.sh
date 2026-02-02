#!/bin/bash

# 🎯 BVRGym - Complete Setup & Training Script
# Run this script to verify and start training

cd /home/neosoft/Documents/BVRGym

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        BVRGym AI Training Environment Setup                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check Python
echo "[1/5] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python3 not found. Install with: sudo apt-get install python3"
    exit 1
fi

# Step 2: Check Virtual Environment
echo ""
echo "[2/5] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "✓ Virtual environment activated"

# Step 3: Install Dependencies
echo ""
echo "[3/5] Installing dependencies (this may take a few minutes)..."
pip install -q --upgrade pip setuptools wheel 2>/dev/null
pip install -q gymnasium jsbsim pymap3d pandas py_trees stable_baselines3 tensorboard torch 2>/dev/null
echo "✓ Dependencies installed"

# Step 4: Verify Syntax
echo ""
echo "[4/5] Verifying code syntax..."
python3 -m py_compile main.py jsb_gym/envs/BaseEnv.py jsb_gym/agents/agents.py jsb_gym/bts/bts.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ All files have correct syntax"
else
    echo "✗ Syntax error found. Check files."
    exit 1
fi

# Step 5: Quick Test
echo ""
echo "[5/5] Running quick verification test..."
python3 test_setup.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  ✓ SETUP COMPLETE - Ready to start training!              ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📌 NEXT STEPS:"
    echo ""
    echo "  1. Start training:"
    echo "     python3 main.py"
    echo ""
    echo "  2. Monitor progress (new terminal):"
    echo "     tensorboard --logdir=runs"
    echo "     Then open: http://localhost:6006"
    echo ""
    echo "  3. Information files:"
    echo "     • QUICK_START.md - Quick reference"
    echo "     • IMPROVEMENTS_SUMMARY.md - Detailed changes"
    echo "     • README.md - Original documentation"
    echo ""
    echo "⏱️  Note: Training will take several HOURS to complete."
    echo "   Keep the terminal running or run in background:"
    echo "   nohup python3 main.py > training.log 2>&1 &"
    echo ""
else
    echo "✗ Verification test failed. Check error above."
    exit 1
fi
