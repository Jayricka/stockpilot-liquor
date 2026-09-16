#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

cd "$BACKEND_DIR"

echo "Running Django checks..."
python manage.py check

echo
echo "Running test suite..."
python manage.py test

echo
echo "All checks and tests passed."
