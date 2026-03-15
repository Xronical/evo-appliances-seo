#!/bin/bash
# Complete Email Sorting System for Evo Appliances
# Creates folders and sorts all emails by category

HIMALAYA="/root/.cargo/bin/himalaya"

echo "=== Evo Appliances Email Organizer ==="
echo ""

# Create folders if they don't exist
FOLDERS=("SEO-Tools" "Social-Media" "Customers" "Hosting" "Industry" "Notifications" "Archive")
for FOLDER in "${FOLDERS[@]}"; do
    $HIMALAYA folder create "$FOLDER" 2>/dev/null || echo "  $FOLDER folder ready"
done

echo ""
echo "=== Sorting Emails ==="
echo ""

# Function to move emails by sender pattern
move_emails_by_sender() {
    local SENDER_PATTERN=$1
    local TARGET_FOLDER=$2
    local IDS=$($HIMALAYA envelope list --page-size 100 -o plain 2>/dev/null | grep -i "$SENDER_PATTERN" | awk -F'|' '{print $2}' | tr -d ' ')
    
    if [ -n "$IDS" ]; then
        echo "Moving emails from '$SENDER_PATTERN' to $TARGET_FOLDER..."
        $HIMALAYA message move "$TARGET_FOLDER" $IDS 2>/dev/null
        echo "  Done"
    fi
}

# 1. SEO-Tools: Ahrefs, Elementor, WPBeginner, Brave, Kimi
move_emails_by_sender "Ahrefs Site Audit" "SEO-Tools"
move_emails_by_sender "Elementor" "SEO-Tools"
move_emails_by_sender "WPBeginner" "SEO-Tools"
move_emails_by_sender "Brave Search API" "SEO-Tools"
move_emails_by_sender "Kimi by Moonshot AI" "SEO-Tools"

# 2. Social-Media: Pinterest, LinkedIn, Instagram
move_emails_by_sender "Pinterest" "Social-Media"
move_emails_by_sender "LinkedIn" "Social-Media"
move_emails_by_sender "Instagram" "Social-Media"

# 3. Customers: Emails with "Re:" (replies) from non-company addresses
# These are actual customer emails
move_emails_by_sender "Sutton Group" "Customers"
move_emails_by_sender "Wayne Huang" "Customers"
move_emails_by_sender "Ann Hosein" "Customers"
move_emails_by_sender "Tal" "Customers"
move_emails_by_sender "Clayton Brown" "Customers"
move_emails_by_sender "Keith" "Customers"
move_emails_by_sender "Carmine M" "Customers"

# 4. Hosting: Hostinger
move_emails_by_sender "Hostinger" "Hosting"

# 5. Industry: Appliance industry related
move_emails_by_sender "Miele Canada" "Industry"
move_emails_by_sender "Havri" "Industry"

# 6. Notifications: Netflix, Medium, other subscriptions
move_emails_by_sender "Netflix" "Notifications"
move_emails_by_sender "Medium" "Notifications"
move_emails_by_sender "login from" "Notifications"

# 7. Postiz (already handled separately, but just in case)
move_emails_by_sender "Nevo From Postiz" "POSTIZ"

echo ""
echo "=== Email Organization Complete ==="
echo ""
echo "Folders created:"
echo "  📧 SEO-Tools (Ahrefs, Elementor, WPBeginner, etc.)"
echo "  📱 Social-Media (Pinterest, LinkedIn, Instagram)"
echo "  👥 Customers (Client emails)"
echo "  🖥️  Hosting (Hostinger)"
echo "  🏭 Industry (Miele, Havri)"
echo "  🔔 Notifications (Netflix, Medium, login alerts)"
echo "  🗂️  Archive (for old emails)"
echo "  📤 POSTIZ (Postiz notifications)"
