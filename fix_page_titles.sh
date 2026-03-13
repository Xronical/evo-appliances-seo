#!/bin/bash
# Fix long page titles for Evo Appliances

WP_HOST="135.84.181.87"
WP_PORT="27"
WP_USER="rinnt515"
WP_PASS="ema2002!"
WP_PATH="/home/rinnt515/public_html"

echo "=========================================="
echo "  🔧 FIXING LONG PAGE TITLES"
echo "=========================================="
echo ""

update_title() {
    local SLUG=$1
    local TITLE=$2
    
    local ID=$(sshpass -p "$WP_PASS" ssh -p $WP_PORT -o StrictHostKeyChecking=no $WP_USER@$WP_HOST "cd $WP_PATH && wp post list --post_type=page --name=$SLUG --format=json --field=ID 2>/dev/null" | head -1)
    
    if [ -n "$ID" ] && [ "$ID" != "null" ]; then
        sshpass -p "$WP_PASS" ssh -p $WP_PORT -o StrictHostKeyChecking=no $WP_USER@$WP_HOST "cd $WP_PATH && wp post update $ID --post_title=\"$TITLE\" 2>/dev/null"
        echo "   ✅ $SLUG"
        echo "      New: $TITLE (${#TITLE} chars)"
    else
        echo "   ⚠️ Not found: $SLUG"
    fi
}

echo "[1] Location pages..."
update_title "appliance-repair-yaletown-2" "Appliance Repair Yaletown | Same-Day Service"
update_title "appliance-repair-kitsilano" "Appliance Repair Kitsilano | Same-Day"
update_title "appliance-repair-richmond-2" "Appliance Repair Richmond | Same-Day"
update_title "appliance-repair-burnaby-2" "Appliance Repair Burnaby | Same-Day"
update_title "appliance-repair-east-vancouver" "Appliance Repair East Vancouver"
update_title "appliance-repair-vancouver" "Appliance Repair Vancouver | Same-Day"

echo ""
echo "[2] Service pages..."
update_title "oven-repair-vancouver-2" "Oven Repair Vancouver | Same-Day"
update_title "stove-repair-vancouver" "Stove Repair Vancouver | Same-Day"
update_title "dishwasher-repair-vancouver-service" "Dishwasher Repair Vancouver"

echo ""
echo "[3] Troubleshooting pages..."
update_title "ice-maker-not-working-heres-how-to-fix-it-fast" "Ice Maker Not Working? | Vancouver"
update_title "why-wont-my-dishwasher-drain-5-fixes-that-actually-work" "Dishwasher Won't Drain? 5 Fixes"
update_title "dryer-not-heating-heres-how-to-fix-it-fast-2025-guide" "Dryer Not Heating? 2025 Guide"
update_title "why-your-dishwasher-wont-drain-5-easy-fixes-that-actually-work" "Dishwasher Won't Drain? 5 Fixes"
update_title "dryer-not-heating-heres-how-to-troubleshoot-before-calling-the-pros" "Dryer Not Heating? Troubleshooting"
update_title "refrigerator-repair-signs-vancouver" "5 Fridge Repair Signs | Vancouver"
update_title "gas-oven-not-heating-safe-troubleshooting-for-vancouver-homeowners" "Gas Oven Not Heating? Troubleshooting"
update_title "why-your-dishwasher-leaves-dishes-dirty-vancouver-repair-guide" "Dishwasher Leaves Dishes Dirty?"
update_title "refrigerator-not-cooling-emergency-repair-guide-for-vancouver-homes" "Fridge Not Cooling? Emergency Guide"
update_title "washing-machine-wont-drain-5-diy-checks-before-calling-a-pro" "Washer Won't Drain? 5 DIY Checks"
update_title "oven-wont-heat-up-5-quick-fixes-to-try-before-calling-the-pros" "Oven Won't Heat? 5 Quick Fixes"
update_title "refrigerator-not-cooling-7-quick-fixes-to-try-before-you-call-a-repair-technician" "Fridge Not Cooling? 7 Quick Fixes"
update_title "washing-machine-making-loud-noise-vancouver" "Washer Loud Noise? Repair | Vancouver"
update_title "dryer-not-heating-4-common-causes-quick-fixes" "Dryer Not Heating? 4 Causes & Fixes"
update_title "5-signs-your-fridge-needs-immediate-repair-before-food-spoils" "5 Fridge Repair Signs | Vancouver"

echo ""
echo "[4] Guide pages..."
update_title "affordable-appliance-repair-in-vancouver-2026-pricing-guide-money-saving-tips" "Affordable Appliance Repair Vancouver 2026"
update_title "affordable-appliance-repair-vancouver-guide" "Affordable Appliance Repair Guide"
update_title "affordable-appliance-repair-vancouver-burnaby-richmond-guide" "Affordable Appliance Repair Guide"
update_title "best-appliance-repair-vancouver-guide" "Best Appliance Repair Vancouver Guide"
update_title "appliance-repair-richmond-common-problems" "Appliance Repair Richmond | Problems"
update_title "sunday-appliance-maintenance-quick-checks-that-save-money" "Sunday Appliance Maintenance Tips"
update_title "need-appliance-repair-near-you-same-day-service-in-vancouver" "Need Appliance Repair Near You?"

echo ""
echo "=========================================="
echo "  ✅ PAGE TITLES OPTIMIZED!"
echo "=========================================="
