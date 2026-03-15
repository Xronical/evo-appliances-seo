#!/bin/bash
# Postiz Email Auto-Filter
# Runs daily to move Postiz emails to POSTIZ folder

HIMALAYA="/root/.cargo/bin/himalaya"

# Get Postiz email IDs from INBOX (grep for "Nevo From Postiz")
POSTIZ_IDS=$($HIMALAYA envelope list --page-size 100 -o plain 2>/dev/null | grep "Nevo From Postiz" | awk -F'|' '{print $2}' | tr -d ' ')

if [ -n "$POSTIZ_IDS" ]; then
    # Move all Postiz emails to POSTIZ folder
    $HIMALAYA message move POSTIZ $POSTIZ_IDS 2>/dev/null
    echo "$(date): Moved Postiz emails to POSTIZ folder" >> /var/log/postiz-filter.log
fi
