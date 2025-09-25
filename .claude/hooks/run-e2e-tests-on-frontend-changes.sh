#!/bin/bash

# Hook script to run E2E tests when frontend files are modified
# This script is triggered after Edit, MultiEdit, or Write operations

# Get the current working directory
PROJECT_ROOT=$(pwd)

# Check if we're in the project root (has both frontend and backend directories)
if [[ ! -d "frontend" || ! -d "backend" ]]; then
    exit 0
fi

# Get the list of recently modified files from git (last 1 minute)
RECENT_FILES=$(find frontend/ -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" 2>/dev/null | head -10)

# If no frontend files found, exit silently
if [[ -z "$RECENT_FILES" ]]; then
    exit 0
fi

# Check if any frontend files were recently modified
FRONTEND_MODIFIED=false
for file in $RECENT_FILES; do
    if [[ $file == frontend/* ]]; then
        FRONTEND_MODIFIED=true
        break
    fi
done

# If frontend files were modified, trigger E2E tests
if [[ "$FRONTEND_MODIFIED" == "true" ]]; then
    echo "🔍 Frontend changes detected, triggering E2E tests with Playwright..."

    # Create a simple message for Claude to trigger the qa-criteria-validator agent
    echo "Frontend files have been modified. Please run E2E tests using the qa-criteria-validator agent to validate the changes with Playwright tests."

    # Log the action
    echo "[$(date)] E2E test trigger activated due to frontend changes" >> .claude/logs/e2e-test-triggers.log 2>/dev/null || true
fi

exit 0