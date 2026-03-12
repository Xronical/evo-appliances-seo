#!/bin/bash
# Apply optimized meta descriptions to all Evo Appliances pages

WP_HOST="135.84.181.87"
WP_PORT="27"
WP_USER="rinnt515"
WP_PASS="ema2002!"
WP_PATH="/home/rinnt515/public_html"

echo "=========================================="
echo "  📝 APPLYING OPTIMIZED META DESCRIPTIONS"
echo "=========================================="
echo ""

# Function to update meta for a page
update_meta() {
    local SLUG=$1
    local META=$2
    
    # Get page ID from slug
    local ID=$(sshpass -p "$WP_PASS" ssh -p $WP_PORT -o StrictHostKeyChecking=no $WP_USER@$WP_HOST "cd $WP_PATH && wp post list --post_type=page --name=$SLUG --format=json --field=ID 2>/dev/null" | head -1)
    
    if [ -n "$ID" ] && [ "$ID" != "null" ]; then
        # Update Yoast
        sshpass -p "$WP_PASS" ssh -p $WP_PORT -o StrictHostKeyChecking=no $WP_USER@$WP_HOST "cd $WP_PATH && wp post meta update $ID _yoast_wpseo_metadesc '$META' 2>/dev/null"
        # Update AIOSEO
        sshpass -p "$WP_PASS" ssh -p $WP_PORT -o StrictHostKeyChecking=no $WP_USER@$WP_HOST "cd $WP_PATH && wp post meta update $ID _aioseo_description '$META' 2>/dev/null"
        echo "   ✅ Updated: $SLUG (${#META} chars)"
    else
        echo "   ⚠️ Not found: $SLUG"
    fi
}

# Update all pages
echo "[1] Homepage..."
update_meta "" "Expert appliance repair in Vancouver. Same-day service for fridges, washers, dryers & more. Call Evo Appliances (604) 200-3054 today!"
update_meta "home" "Same-day appliance repair Vancouver. Expert technicians for all brands. Fridges, washers, dryers. Call (604) 200-3054."

echo ""
echo "[2] Location pages..."
update_meta "appliance-repair-mount-pleasant" "Appliance repair Mount Pleasant Vancouver. Same-day service for all brands. Call Evo Appliances (604) 200-3054."
update_meta "appliance-repair-east-vancouver" "Appliance repair East Vancouver. Same-day service for fridges, washers, dryers. Call (604) 200-3054."

echo ""
echo "[3] Service pages..."
update_meta "stove-repair-vancouver" "Stove & oven repair Vancouver. Same-day service. All brands. Call Evo Appliances (604) 200-3054 today!"
update_meta "dishwasher-repair-vancouver-service" "Dishwasher repair Vancouver. Same-day service. All brands fixed. Call Evo Appliances (604) 200-3054!"

echo ""
echo "[4] Troubleshooting pages..."
update_meta "ice-maker-not-working-heres-how-to-fix-it-fast" "Ice maker not working? Fast fixes & repair solutions. Same-day service Vancouver. Call (604) 200-3054."
update_meta "dryer-not-heating-heres-how-to-fix-it-fast-2025-guide" "Dryer not heating? 2025 repair guide & fast fixes. Same-day Vancouver service. Call (604) 200-3054!"
update_meta "why-your-dishwasher-wont-drain-5-easy-fixes-that-actually-work" "Dishwasher won't drain? 5 easy fixes that work. Need help? Same-day repair Vancouver. Call (604) 200-3054!"
update_meta "refrigerator-repair-signs-vancouver" "5 signs your fridge needs repair Vancouver. Same-day service. Call Evo Appliances (604) 200-3054 today!"
update_meta "refrigerator-not-cooling-emergency-repair-guide-for-vancouver-homes" "Fridge not cooling? Emergency repair guide. Same-day Vancouver service. Call (604) 200-3054!"
update_meta "oven-wont-heat-up-5-quick-fixes-to-try-before-calling-the-pros" "Oven won't heat? 5 quick fixes to try. Same-day repair Vancouver. Call (604) 200-3054!"
update_meta "what-to-do-in-an-appliance-emergency" "Appliance emergency? Fast response & same-day repair. Vancouver experts. Call (604) 200-3054 now!"

echo ""
echo "[5] General service..."
update_meta "appliance-repair-vancouver" "Appliance repair Vancouver. Same-day service for fridges, washers, dryers. Call Evo Appliances (604) 200-3054!"

echo ""
echo "=========================================="
echo "  ✅ META DESCRIPTIONS APPLIED!"
echo "=========================================="
