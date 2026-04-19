#!/bin/bash
# One-command setup for ADHD Study Guide project
# Usage: ./setup.sh

set -e  # Exit on error

echo "======================================================================"
echo "🧠 ADHD Study Guide - Setup Script"
echo "======================================================================"

# Check Python version
echo ""
echo "1️⃣ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python 3.8+ required (found $PYTHON_VERSION)"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION detected"

# Check if uv is available (preferred method)
if command -v uv &> /dev/null; then
    echo ""
    echo "2️⃣ Using uv package manager..."

    # Create/sync venv with uv
    if [ ! -d ".venv" ]; then
        uv venv
        echo "✅ Virtual environment created with uv"
    else
        echo "✅ Virtual environment already exists"
    fi

    echo ""
    echo "3️⃣ Installing dependencies with uv..."
    uv pip install -r requirements.txt > /dev/null 2>&1
    echo "✅ Dependencies installed with uv"
else
    # Fallback to standard pip
    echo ""
    echo "2️⃣ Creating virtual environment (standard method)..."
    echo "   Note: Install uv for faster package management: https://docs.astral.sh/uv/"

    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        echo "✅ Virtual environment created"
    else
        echo "✅ Virtual environment already exists"
    fi

    # Activate virtual environment
    echo ""
    echo "3️⃣ Activating virtual environment..."
    source .venv/bin/activate
    echo "✅ Virtual environment activated"

    # Install dependencies
    echo ""
    echo "4️⃣ Installing dependencies with pip..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
    echo "✅ Dependencies installed"
fi

# Check for .env file
echo ""
echo "5️⃣ Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    cat > .env << 'EOF'
# LLM Provider Configuration
LLM_PROVIDER=gemini

# API Keys (add your own)
GEMINI_API_KEY=your_gemini_key_here
AWS_ACCESS_KEY_ID=your_aws_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here
ANTHROPIC_API_KEY=your_anthropic_key_here
EOF
    echo "⚠️  Please edit .env and add your API keys"
    echo "   Then re-run this script"
    exit 0
else
    echo "✅ .env file exists"
fi

# Generate raw data files
echo ""
echo "6️⃣ Setting up data files..."
if [ ! -f "data/golden_dataset.jsonl" ]; then
    echo "   Generating raw excerpts..."
    python3 scripts/generate_raw_files.py
    echo "   Creating golden dataset..."
    python3 data/create_golden_dataset.py
    echo "✅ Golden dataset created"
else
    echo "✅ Golden dataset already exists"
fi

# Run tests
echo ""
echo "7️⃣ Running test suite..."
python3 -m pytest tests/ -v --tb=short

# Success message
echo ""
echo "======================================================================"
echo "✅ Setup complete! "
echo "======================================================================"
echo ""
echo "Quick Start Commands:"
echo ""
echo "  # Launch Streamlit UI"
echo "  streamlit run src/app.py"
echo ""
echo "  # Run evaluation harness"
echo "  python evaluations/run_evaluation.py --provider gemini"
echo ""
echo "  # Run baseline comparison"
echo "  python evaluations/baseline_comparison.py --samples 5"
echo ""
echo "  # Run tests"
echo "  python -m pytest tests/ -v"
echo ""
echo "======================================================================"
