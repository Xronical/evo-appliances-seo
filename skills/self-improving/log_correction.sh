#!/bin/bash
# Log correction to self-improving system
# Usage: log_correction "Error description" "Lesson learned"

ERROR="$1"
LESSON="$2"
TYPE="${3:-correction}"

if [ -z "$ERROR" ] || [ -z "$LESSON" ]; then
    echo "Usage: log_correction 'Error description' 'Lesson learned' [type]"
    exit 1
fi

DATE=$(date '+%Y-%m-%d %H:%M')

echo "- [$DATE] $ERROR
  Type: $TYPE
  Lesson: $LESSON
  Confirmed: pending" >> ~/self-improving/corrections.md

echo "✅ Correction logged to ~/self-improving/corrections.md"
