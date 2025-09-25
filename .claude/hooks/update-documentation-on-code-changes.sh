#!/bin/bash

# Hook script to update documentation when code changes are made
# This script is triggered after Edit, MultiEdit, or Write operations

# Get the current working directory
PROJECT_ROOT=$(pwd)

# Check if we're in the correct project root
if [[ ! -f "CLAUDE.md" ]]; then
    exit 0
fi

# Create logs directory if it doesn't exist
mkdir -p .claude/logs

# Function to log messages
log_message() {
    echo "[$(date)] $1" >> .claude/logs/documentation-updates.log 2>/dev/null || true
}

# Function to check if specific types of files were modified
check_modified_files() {
    local pattern="$1"
    find . -name "$pattern" -newer .claude/last-doc-update 2>/dev/null | head -5
}

# Create timestamp file if it doesn't exist
if [[ ! -f .claude/last-doc-update ]]; then
    touch .claude/last-doc-update
fi

# Check for different types of changes that require documentation updates
BACKEND_CHANGES=$(check_modified_files "*.py")
FRONTEND_CHANGES=$(check_modified_files "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx")
CONFIG_CHANGES=$(check_modified_files "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml")
DATABASE_CHANGES=$(find . -path "*/models/*" -name "*.py" -newer .claude/last-doc-update 2>/dev/null | head -5)
API_CHANGES=$(find . -path "*/routers/*" -name "*.py" -newer .claude/last-doc-update 2>/dev/null | head -5)

# Initialize documentation update messages
DOCS_TO_UPDATE=""

# Check for backend changes
if [[ -n "$BACKEND_CHANGES" ]]; then
    DOCS_TO_UPDATE="$DOCS_TO_UPDATE\n- Backend code changes detected - update API documentation and architecture diagrams"
    log_message "Backend changes detected: $BACKEND_CHANGES"
fi

# Check for frontend changes
if [[ -n "$FRONTEND_CHANGES" ]]; then
    DOCS_TO_UPDATE="$DOCS_TO_UPDATE\n- Frontend code changes detected - update component documentation and user guides"
    log_message "Frontend changes detected: $FRONTEND_CHANGES"
fi

# Check for database/model changes
if [[ -n "$DATABASE_CHANGES" ]]; then
    DOCS_TO_UPDATE="$DOCS_TO_UPDATE\n- Database model changes detected - update data model documentation and ER diagrams"
    log_message "Database model changes detected: $DATABASE_CHANGES"
fi

# Check for API changes
if [[ -n "$API_CHANGES" ]]; then
    DOCS_TO_UPDATE="$DOCS_TO_UPDATE\n- API endpoint changes detected - update API documentation and OpenAPI specs"
    log_message "API endpoint changes detected: $API_CHANGES"
fi

# Check for configuration changes
if [[ -n "$CONFIG_CHANGES" ]]; then
    DOCS_TO_UPDATE="$DOCS_TO_UPDATE\n- Configuration changes detected - update setup and deployment documentation"
    log_message "Configuration changes detected: $CONFIG_CHANGES"
fi

# Check if authentication/security files were modified
AUTH_CHANGES=$(find . -name "*auth*" -o -name "*security*" -o -name "*oauth*" -newer .claude/last-doc-update 2>/dev/null | head -5)
if [[ -n "$AUTH_CHANGES" ]]; then
    DOCS_TO_UPDATE="$DOCS_TO_UPDATE\n- Authentication/security changes detected - update security documentation"
    log_message "Authentication/security changes detected: $AUTH_CHANGES"
fi

# Check if test files were modified
TEST_CHANGES=$(find . -path "*/test*" -name "*.py" -o -path "*/test*" -name "*.ts" -o -path "*/test*" -name "*.tsx" -newer .claude/last-doc-update 2>/dev/null | head -5)
if [[ -n "$TEST_CHANGES" ]]; then
    DOCS_TO_UPDATE="$DOCS_TO_UPDATE\n- Test changes detected - update testing documentation and coverage reports"
    log_message "Test changes detected: $TEST_CHANGES"
fi

# If any changes were detected, output documentation update requirements
if [[ -n "$DOCS_TO_UPDATE" ]]; then
    echo "📚 Code changes detected that require documentation updates:"
    echo -e "$DOCS_TO_UPDATE"
    echo ""
    echo "Please update the following documentation files as needed:"
    echo "- CLAUDE.md (project guidelines and architecture)"
    echo "- TEAM_AGREEMENTS.md (team conventions and processes)"
    echo "- .cursorrules (cursor AI rules and patterns)"
    echo "- API documentation (if API changes were made)"
    echo "- Data model documentation (if database changes were made)"
    echo "- Architecture diagrams (if structural changes were made)"
    echo "- README.md (if setup or usage changed)"

    # Update timestamp
    touch .claude/last-doc-update

    log_message "Documentation update notification sent to user"
else
    log_message "No significant changes detected requiring documentation updates"
fi

# Check if specific documentation files need updates based on file patterns
DOC_SUGGESTIONS=""

# If package.json or poetry.lock changed, suggest updating setup docs
if [[ -n $(find . -name "package.json" -o -name "poetry.lock" -o -name "requirements.txt" -newer .claude/last-doc-update 2>/dev/null) ]]; then
    DOC_SUGGESTIONS="$DOC_SUGGESTIONS\n- Update installation and setup instructions in README.md"
fi

# If docker files changed, suggest updating deployment docs
if [[ -n $(find . -name "Dockerfile" -o -name "docker-compose*" -newer .claude/last-doc-update 2>/dev/null) ]]; then
    DOC_SUGGESTIONS="$DOC_SUGGESTIONS\n- Update Docker deployment documentation"
fi

# If environment files changed, suggest updating configuration docs
if [[ -n $(find . -name ".env*" -o -name "*.env" -newer .claude/last-doc-update 2>/dev/null) ]]; then
    DOC_SUGGESTIONS="$DOC_SUGGESTIONS\n- Update environment configuration documentation"
fi

# Output additional suggestions if any
if [[ -n "$DOC_SUGGESTIONS" ]]; then
    echo "Additional documentation suggestions:"
    echo -e "$DOC_SUGGESTIONS"
fi

exit 0