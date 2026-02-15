#!/bin/bash
# Setup script for Decoy Service

echo "=========================================="
echo "Decoy Service - Setup Script"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment (optional but recommended)
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup Playwright browsers (if using Playwright)
echo ""
echo "Setting up Playwright browsers (optional)..."
read -p "Install Playwright browsers? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    playwright install
fi

# Create .env file from template
echo ""
echo "Setting up configuration..."
if [ ! -f config/.env ]; then
    cp config/.env.example config/.env
    echo "Created config/.env - please edit with your settings"
fi

# Create logs directory
mkdir -p logs

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit config/settings.yaml to customize behavior"
echo "2. Edit config/websites.yaml to add/remove websites"
echo "3. Run: python decoy_service.py"
echo ""
echo "For scheduled sessions, run: python scheduler.py"
echo ""
