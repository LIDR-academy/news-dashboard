#!/bin/bash

# Documentation Synchronization Checker
# This script detects when documentation might be out of sync with code changes

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Checking documentation synchronization...${NC}\n"

# Function to check if files have been modified
check_changes() {
    local pattern="$1"
    local description="$2"
    
    if git diff --cached --name-only | grep -E "$pattern" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  $description${NC}"
        git diff --cached --name-only | grep -E "$pattern" | sed 's/^/   - /'
        return 0
    fi
    return 1
}

# Function to suggest documentation updates
suggest_update() {
    local file="$1"
    local reason="$2"
    
    echo -e "${YELLOW}💡 Consider updating: ${BLUE}$file${NC}"
    echo -e "   Reason: $reason\n"
}

# Check for API changes
echo -e "${BLUE}📡 Checking API changes...${NC}"
if check_changes "(router|endpoint|api|dto)" "API-related files changed"; then
    suggest_update "OpenAPI/Swagger documentation" "API endpoints or DTOs modified"
    suggest_update "README.md API section" "API usage patterns might have changed"
fi

# Check for architectural changes
echo -e "${BLUE}🏗️  Checking architectural changes...${NC}"
if check_changes "(src/domain|src/application|src/infrastructure)" "Core architecture files changed"; then
    suggest_update ".cursorrules" "New architectural patterns might have emerged"
    suggest_update "Architecture diagrams" "System structure might have changed"
fi

# Check for new features
echo -e "${BLUE}🆕 Checking new features...${NC}"
if check_changes "src/features/[^/]+/[^/]+\.(ts|tsx|py)$" "New feature files added"; then
    suggest_update "Feature documentation" "New features should be documented"
    suggest_update "README.md features section" "New capabilities added to system"
fi

# Check for dependency changes
echo -e "${BLUE}📦 Checking dependency changes...${NC}"
if check_changes "(package\.json|pyproject\.toml|requirements\.txt)" "Dependencies changed"; then
    suggest_update "README.md setup section" "Installation/setup instructions might need updates"
    suggest_update "Development environment docs" "New tools or versions might affect setup"
fi

# Check for test changes that might indicate new patterns
echo -e "${BLUE}🧪 Checking test patterns...${NC}"
if check_changes "__tests__|test_.*\.py" "Test files changed"; then
    # Count new test files
    new_tests=$(git diff --cached --name-only | grep -E "__tests__|test_.*\.py" | wc -l)
    if [ "$new_tests" -gt 5 ]; then
        suggest_update ".cursorrules testing section" "Significant test changes might indicate new patterns"
    fi
fi

# Check for configuration changes
echo -e "${BLUE}⚙️  Checking configuration changes...${NC}"
if check_changes "(config|\.env|docker|nginx|Dockerfile)" "Configuration files changed"; then
    suggest_update "Deployment documentation" "Infrastructure or config changes detected"
    suggest_update "README.md setup section" "Environment configuration might have changed"
fi

# Check for new patterns in recent commits (if not in pre-commit)
if [ "$1" != "--pre-commit" ]; then
    echo -e "${BLUE}🔄 Checking recent patterns...${NC}"
    
    # Look for repeated terms in recent commit messages that might indicate new patterns
    repeated_terms=$(git log --oneline --since="2 weeks ago" | \
                    grep -oE '\b[A-Z][a-z]+\b' | \
                    sort | uniq -c | sort -nr | head -5)
    
    if [ -n "$repeated_terms" ]; then
        echo -e "${YELLOW}📊 Frequently mentioned terms in recent commits:${NC}"
        echo "$repeated_terms" | while read count term; do
            if [ "$count" -gt 3 ]; then
                echo "   - $term (mentioned $count times)"
            fi
        done
        echo -e "\n${YELLOW}💡 Consider if these patterns need documentation${NC}\n"
    fi
fi

# Check for README staleness
echo -e "${BLUE}📚 Checking README freshness...${NC}"
if [ -f "README.md" ]; then
    readme_age=$(git log -1 --format="%ct" README.md 2>/dev/null || echo "0")
    current_time=$(date +%s)
    age_days=$(( (current_time - readme_age) / 86400 ))
    
    if [ "$age_days" -gt 30 ]; then
        echo -e "${YELLOW}📅 README.md hasn't been updated in $age_days days${NC}"
        suggest_update "README.md" "Consider reviewing for accuracy and completeness"
    fi
fi

# Summary
echo -e "${GREEN}✅ Documentation sync check complete!${NC}\n"

# If this is a pre-commit hook, exit with error if critical docs are missing
if [ "$1" = "--pre-commit" ]; then
    # Check for critical API changes without doc updates
    if git diff --cached --name-only | grep -E "(router|endpoint)" > /dev/null && \
       ! git diff --cached --name-only | grep -E "(README|openapi|swagger|\.md)" > /dev/null; then
        echo -e "${RED}❌ BLOCKING: API changes detected but no documentation updates found${NC}"
        echo -e "${YELLOW}Please update relevant documentation before committing${NC}"
        exit 1
    fi
fi

exit 0
