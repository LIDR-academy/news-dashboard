#!/bin/bash

# Manual documentation update trigger
# Use this script to manually check what documentation needs updating

echo "🔍 Checking for documentation update requirements..."

# Reset the timestamp to force checking all files
rm -f .claude/last-doc-update 2>/dev/null

# Run the documentation update check
.claude/hooks/update-documentation-on-code-changes.sh

echo ""
echo "✅ Documentation update check completed"
echo "Check the output above for specific documentation that needs updating"