#!/bin/bash

# Graph Cities - Setup Script
set -e

echo "🌐 Graph Cities - Setup"
echo "======================"

# Check Python version
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "✅ Python 3.8+ detected"
else
    echo "❌ Python 3.8+ required"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
[ -d "venv" ] && rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Install test dependencies (optional)
echo "📥 Installing test dependencies (optional)..."
pip install --upgrade pip
pip install pytest

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate: source venv/bin/activate"
echo "To run demo: python examples/main.py"
echo "To run tests: pytest tests/"
