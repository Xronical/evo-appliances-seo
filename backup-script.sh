#!/bin/bash
# Evo Appliances - Weekly GitHub Backup Script
# /root/.openclaw/workspace/backup-script.sh

set -e

cd /root/.openclaw/workspace

echo "=== Evo Appliances Backup - $(date '+%Y-%m-%d %H:%M:%S') ==="

# Check git status
echo "Checking git status..."
git status --short

# Add all changes
echo "Adding all changes..."
git add -A

# Get list of files being backed up
FILES_BACKEDUP=$(git diff --cached --name-only | wc -l)

if [ "$FILES_BACKEDUP" -eq 0 ]; then
    echo "No changes to commit. Backup skipped."
    exit 0
fi

echo "Files to backup: $FILES_BACKEDUP"
git diff --cached --name-only

# Commit with timestamp
COMMIT_MSG="Weekly backup - $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Committing: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# Push to GitHub
echo "Pushing to GitHub..."
git push origin master

# Get commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)
echo "=== Backup Complete ==="
echo "Commit: $COMMIT_HASH"
echo "Files: $FILES_BACKEDUP"
