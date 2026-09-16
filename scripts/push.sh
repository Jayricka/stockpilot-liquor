#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
    echo 'Usage: ./scripts/push.sh "commit message"'
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

echo "Running tests before push..."
./scripts/test.sh

echo
echo "Staging changes..."
git add .

echo
echo "Creating commit..."
git commit -m "$1"

BRANCH="$(git branch --show-current)"

echo
echo "Pushing branch: $BRANCH..."
git push -u origin "$BRANCH"

echo
echo "Push completed successfully."
