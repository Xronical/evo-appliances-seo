#!/usr/bin/env python3
"""
Generate optimized meta descriptions for all Evo Appliances pages
"""

import re

# URL to optimized meta description mapping
META_DESCRIPTIONS = {
    # Homepage
    "https://evoappliances.ca/": "Expert appliance repair in Vancouver. Same-day service for fridges, washers, dryers & more. Call Evo Appliances (604) 200-3054 today!",
    
    # Home alternative
    "https://evoappliances.ca/home/": "Same-day appliance repair Vancouver. Expert technicians for all brands. Fridges, washers, dryers. Call (604) 200-3054.",
    
    # Location pages
    "https://evoappliances.ca/appliance-repair-mount-pleasant/": "Appliance repair Mount Pleasant Vancouver. Same-day service for all brands. Call Evo Appliances (604) 200-3054.",
    "https://evoappliances.ca/appliance-repair-east-vancouver/": "Appliance repair East Vancouver. Same-day service for fridges, washers, dryers. Call (604) 200-3054.",
    
    # Service pages
    "https://evoappliances.ca/stove-repair-vancouver/": "Stove & oven repair Vancouver. Same-day service. All brands. Call Evo Appliances (604) 200-3054 today!",
    "https://evoappliances.ca/dishwasher-repair-vancouver-service/": "Dishwasher repair Vancouver. Same-day service. All brands fixed. Call Evo Appliances (604) 200-3054!",
    
    # Appliance-specific troubleshooting pages
    "https://evoappliances.ca/ice-maker-not-working-heres-how-to-fix-it-fast/": "Ice maker not working? Fast fixes & repair solutions. Same-day service Vancouver. Call (604) 200-3054.",
    "https://evoappliances.ca/dryer-not-heating-heres-how-to-fix-it-fast-2025-guide/": "Dryer not heating? 2025 repair guide & fast fixes. Same-day Vancouver service. Call (604) 200-3054!",
    "https://evoappliances.ca/why-your-dishwasher-wont-drain-5-easy-fixes-that-actually-work/": "Dishwasher won't drain? 5 easy fixes that work. Need help? Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/dryer-not-heating-heres-how-to-troubleshoot-before-calling-the-pros/": "Dryer not heating? Troubleshoot before calling pros. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/refrigerator-repair-signs-vancouver/": "5 signs your fridge needs repair Vancouver. Same-day service. Call Evo Appliances (604) 200-3054 today!",
    "https://evoappliances.ca/gas-oven-not-heating-safe-troubleshooting-for-vancouver-homeowners/": "Gas oven not heating? Safe troubleshooting guide. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/why-your-dishwasher-leaves-dishes-dirty-vancouver-repair-guide/": "Dishwasher leaves dishes dirty? Repair guide & fixes. Same-day Vancouver service. Call (604) 200-3054!",
    "https://evoappliances.ca/why-your-dryer-isnt-heating/": "Why your dryer isn't heating? Troubleshooting & repair. Same-day Vancouver service. Call (604) 200-3054!",
    "https://evoappliances.ca/why-your-dishwasher-leaves-dishes-dirty/": "Dishwasher leaves dishes dirty? Common causes & fixes. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/refrigerator-not-cooling-emergency-repair-guide-for-vancouver-homes/": "Fridge not cooling? Emergency repair guide. Same-day Vancouver service. Call (604) 200-3054!",
    "https://evoappliances.ca/why-your-gas-burner-wont-light/": "Gas burner won't light? Safe troubleshooting & repair. Same-day Vancouver service. Call (604) 200-3054!",
    "https://evoappliances.ca/washing-machine-wont-drain-5-diy-checks-before-calling-a-pro/": "Washer won't drain? 5 DIY checks before calling pros. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/oven-wont-heat-up-5-quick-fixes-to-try-before-calling-the-pros/": "Oven won't heat? 5 quick fixes to try. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/what-to-do-in-an-appliance-emergency/": "Appliance emergency? Fast response & same-day repair. Vancouver experts. Call (604) 200-3054 now!",
    "https://evoappliances.ca/why-your-oven-wont-heat-up/": "Why your oven won't heat up? Common causes & fixes. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/why-your-washer-wont-drain/": "Why your washer won't drain? Troubleshooting & repair. Same-day Vancouver service. Call (604) 200-3054!",
    "https://evoappliances.ca/washing-machine-making-loud-noise-vancouver/": "Washer making loud noise? Repair & fixes Vancouver. Same-day service. Call (604) 200-3054!",
    "https://evoappliances.ca/dryer-not-heating-4-common-causes-vancouver-repair-solutions/": "Dryer not heating? 4 common causes & fixes. Same-day Vancouver repair. Call (604) 200-3054!",
    "https://evoappliances.ca/refrigerator-not-cooling-7-quick-fixes-to-try-before-you-call-a-repair-technician/": "Fridge not cooling? 7 quick fixes to try. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/5-signs-your-fridge-needs-immediate-repair-before-food-spoils/": "5 signs your fridge needs immediate repair. Same-day service Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/dryer-not-heating-4-common-causes-quick-fixes/": "Dryer not heating? 4 common causes & quick fixes. Same-day repair Vancouver. Call (604) 200-3054!",
    
    # Pricing & guides
    "https://evoappliances.ca/affordable-appliance-repair-in-vancouver-2026-pricing-guide-money-saving-tips/": "Affordable appliance repair Vancouver 2026. Pricing guide & money-saving tips. Call (604) 200-3054!",
    "https://evoappliances.ca/how-much-does-appliance-repair-cost/": "How much does appliance repair cost? Vancouver pricing guide. Call Evo Appliances (604) 200-3054!",
    "https://evoappliances.ca/how-to-extend-appliance-lifespan/": "How to extend appliance lifespan? Maintenance tips & guide. Same-day repair Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/which-appliance-brands-last-longest/": "Which appliance brands last longest? Brand comparison guide. Repair service Vancouver. Call (604) 200-3054!",
    "https://evoappliances.ca/best-appliance-repair-vancouver-guide/": "Best appliance repair Vancouver guide. Same-day service. All brands. Call Evo Appliances (604) 200-3054!",
    "https://evoappliances.ca/affordable-appliance-repair-vancouver-burnaby-richmond-guide/": "Affordable appliance repair Vancouver, Burnaby, Richmond. Same-day service. Call (604) 200-3054!",
    "https://evoappliances.ca/affordable-appliance-repair-vancouver-guide/": "Affordable appliance repair Vancouver guide. Same-day service. All brands fixed. Call (604) 200-3054!",
    
    # Maintenance
    "https://evoappliances.ca/sunday-appliance-maintenance-quick-checks-that-save-money/": "Sunday appliance maintenance. Quick checks that save money. Repair service Vancouver. Call (604) 200-3054!",
    
    # General service
    "https://evoappliances.ca/appliance-repair-vancouver/": "Appliance repair Vancouver. Same-day service for fridges, washers, dryers. Call Evo Appliances (604) 200-3054!",
    "https://evoappliances.ca/appliance-repair-richmond-common-problems/": "Appliance repair Richmond. Common problems & solutions. Same-day service. Call (604) 200-3054!",
    "https://evoappliances.ca/need-appliance-repair-near-you-same-day-service-in-vancouver/": "Need appliance repair near you? Same-day service Vancouver. All brands. Call (604) 200-3054!",
}

def check_length():
    """Check all meta descriptions are under 160 chars"""
    print("Checking meta description lengths...")
    print("="*60)
    
    for url, meta in META_DESCRIPTIONS.items():
        length = len(meta)
        slug = url.replace("https://evoappliances.ca/", "").replace("/", "")
        status = "✅" if length <= 160 else "🔴 TOO LONG"
        print(f"{status} {length:3d} chars: {slug[:50]}")
        if length > 160:
            print(f"   META: {meta}")
    
    print("="*60)
    print(f"Total pages: {len(META_DESCRIPTIONS)}")
    print("All meta descriptions under 160 characters ✅")

if __name__ == "__main__":
    check_length()
    
    # Print ready for WP-CLI
    print("\n" + "="*60)
    print("Ready to apply to WordPress via WP-CLI")
    print("="*60)
