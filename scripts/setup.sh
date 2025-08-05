#!/bin/bash

echo "🔍 Checking for required tools..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it: https://www.python.org/downloads/"
    exit 1
else
    echo "✅ Python 3 found: $(python3 --version)"
fi

# Check pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip not found. You may need to reinstall Python or run: curl https://bootstrap.pypa.io/get-pip.py | python3"
    exit 1
else
    echo "✅ pip found"
fi

# Check venv
if ! python3 -m venv --help &> /dev/null; then
    echo "❌ venv module not available. You may need to install python3-venv or reinstall Python."
    exit 1
else
    echo "✅ venv module available"
fi

# Check for requirements.txt
if [ ! -f requirements.txt ]; then
    echo "❌ requirements.txt not found in current directory."
    exit 1
else
    echo "✅ requirements.txt found"
fi

# Check for script
if [ ! -f scrape_events.py ]; then
    echo "❌ scrape_events.py not found."
    exit 1
else
    echo "✅ Scraper script found"
fi

# Check credentials file
if [ ! -f credentials.json ]; then
    echo "❌ credentials.json not found. Please place your service account key in this file."
    exit 1
else
    echo "✅ Google credentials file found"
fi

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv env
else
    echo "✅ Virtual environment already exists."
fi

# Step 2: Activate the virtual environment
source env/bin/activate
echo "✅ Virtual environment is now active: $VIRTUAL_ENV"

# Step 3: Install required packages
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Step 4: Run the scraper
echo "🚀 Running scraper..."
python scraper_DSA.py

# Check if it succeeded
if [ $? -eq 0 ]; then
    echo "✅ Scraper completed successfully!"
else
    echo "❌ Scraper failed. Check for errors above."
fi

echo "✅ Scraper finished at $(date)"