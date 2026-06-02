#!/bin/bash

# UDISE+ Student Progression Automation - Quick Setup Script
# This script sets up the project with all dependencies

set -e

echo "📦 UDISE+ Automation - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python $PYTHON_VERSION found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📁 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install -q chromium

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "   Creating .env from template..."
    cp .env.example .env
    echo "   ⚠️  Please update .env with your UDISE+ credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Update credentials in .env file"
echo "   2. Run: source venv/bin/activate"
echo "   3. Run: python3 -m src.main"
echo ""
