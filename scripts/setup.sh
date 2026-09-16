#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$PROJECT_ROOT/backend"

echo "Setting up StockPilot Liquor..."

cd "$BACKEND"

if [ ! -d "myenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myenv
fi

source myenv/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Applying migrations..."
python manage.py migrate

echo
echo "Setup complete."
echo "Activate the environment with:"
echo "source backend/myenv/bin/activate"
