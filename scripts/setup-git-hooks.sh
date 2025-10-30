#!/bin/bash

# Git Hooks Setup for Documentation Automation
# Run this script to set up automated documentation checks

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🪝 Setting up git hooks for documentation automation...${NC}\n"

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Pre-commit hook for documentation validation
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Pre-commit hook: Documentation synchronization check
# This runs before each commit to ensure docs stay in sync

echo "🔍 Running pre-commit documentation checks..."

# Run the documentation sync checker in pre-commit mode
./scripts/check-docs-sync.sh --pre-commit

# Check for common documentation issues
echo "📝 Checking for documentation quality..."

# Ensure all Python functions have docstrings (in modified files)
python_files_changed=$(git diff --cached --name-only | grep '\.py$' || true)
if [ -n "$python_files_changed" ]; then
    for file in $python_files_changed; do
        if git diff --cached "$file" | grep -E "^+\s*def " > /dev/null; then
            # New function added, check if it has docstring
            if ! git show ":$file" | grep -A 3 "def " | grep -E '"""|\'\'\'' > /dev/null; then
                echo "⚠️  Warning: New function in $file might be missing docstring"
            fi
        fi
    done
fi

# Check for TODO comments that mention documentation
todos=$(git diff --cached | grep -E "^\+.*TODO.*doc" || true)
if [ -n "$todos" ]; then
    echo "📋 Found TODO items related to documentation:"
    echo "$todos"
    echo "💡 Consider addressing these before committing"
fi

echo "✅ Pre-commit documentation checks complete"
EOF

# Post-commit hook for documentation reminders
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash

# Post-commit hook: Documentation maintenance reminders
# This runs after each commit to provide helpful reminders

# Get the commit message
commit_msg=$(git log -1 --pretty=%B)

# Check if this was a significant change that might need doc updates
if echo "$commit_msg" | grep -iE "(feat|feature|breaking|major)" > /dev/null; then
    echo ""
    echo "🎉 Significant change committed! Consider updating:"
    echo "   📖 README.md - if user-facing changes"
    echo "   🏗️  Architecture docs - if structural changes"
    echo "   📚 .cursorrules - if new patterns emerged"
    echo ""
fi

# Check if we're approaching documentation review time
last_cursorrules_update=$(git log -1 --format="%ct" .cursorrules 2>/dev/null || echo "0")
current_time=$(date +%s)
days_since_update=$(( (current_time - last_cursorrules_update) / 86400 ))

if [ "$days_since_update" -gt 60 ]; then
    echo "📅 Reminder: .cursorrules last updated $days_since_update days ago"
    echo "   Consider reviewing for new patterns or team changes"
    echo ""
fi
EOF

# Prepare-commit-msg hook for conventional commits
cat > .git/hooks/prepare-commit-msg << 'EOF'
#!/bin/bash

# Prepare-commit-msg hook: Help with conventional commits and doc reminders

commit_file="$1"
commit_source="$2"

# Only run for regular commits (not merges, etc.)
if [ "$commit_source" = "" ]; then
    # Check if any documentation files are being committed
    doc_files=$(git diff --cached --name-only | grep -E '\.(md|rst)$' || true)
    
    if [ -n "$doc_files" ]; then
        # Add a reminder comment to the commit message
        echo "" >> "$commit_file"
        echo "# Documentation files updated:" >> "$commit_file"
        echo "$doc_files" | sed 's/^/# - /' >> "$commit_file"
        echo "#" >> "$commit_file"
        echo "# Consider: docs(scope): brief description of what was documented" >> "$commit_file"
    fi
    
    # Check for API changes and suggest appropriate commit message
    api_files=$(git diff --cached --name-only | grep -E "(router|endpoint|api)" || true)
    if [ -n "$api_files" ]; then
        echo "#" >> "$commit_file"
        echo "# API files changed - consider conventional commit types:" >> "$commit_file"
        echo "# feat(api): for new endpoints" >> "$commit_file"
        echo "# fix(api): for bug fixes" >> "$commit_file"
        echo "# refactor(api): for restructuring" >> "$commit_file"
        echo "# BREAKING CHANGE: for breaking changes" >> "$commit_file"
    fi
fi
EOF

# Make all hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit
chmod +x .git/hooks/prepare-commit-msg

echo -e "${GREEN}✅ Git hooks installed successfully!${NC}\n"

echo -e "${BLUE}📋 Installed hooks:${NC}"
echo -e "   🔍 ${YELLOW}pre-commit${NC}: Validates documentation sync before commits"
echo -e "   🎉 ${YELLOW}post-commit${NC}: Provides reminders after significant changes"
echo -e "   💬 ${YELLOW}prepare-commit-msg${NC}: Helps with conventional commit messages"

echo -e "\n${BLUE}🔧 Manual usage:${NC}"
echo -e "   ${YELLOW}./scripts/check-docs-sync.sh${NC} - Run documentation sync check anytime"
echo -e "   ${YELLOW}git commit${NC} - Hooks will run automatically"

echo -e "\n${GREEN}🎯 Benefits:${NC}"
echo -e "   • Automatic detection of doc/code drift"
echo -e "   • Reminders for documentation updates"
echo -e "   • Better commit message consistency"
echo -e "   • Proactive documentation maintenance"

echo -e "\n${BLUE}💡 Pro tip:${NC} Run ${YELLOW}./scripts/check-docs-sync.sh${NC} periodically to catch documentation drift early!"
