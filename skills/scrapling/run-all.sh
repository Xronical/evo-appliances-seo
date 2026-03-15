#!/bin/bash
# Scrapling Master Script - Run all Scrapling tasks
# Usage: ./run-all.sh [competitor|reviews|content|all]

SCRIPT_DIR="/root/.openclaw/workspace/skills/scrapling"
DATA_DIR="/root/.openclaw/workspace/data"

echo "=========================================="
echo "  Evo Appliances - Scrapling Automation"
echo "=========================================="
echo ""

# Create data directory if not exists
mkdir -p "$DATA_DIR"

# Function to run script with error handling
run_script() {
    local script_name=$1
    local script_path="$SCRIPT_DIR/$script_name"
    
    echo "🔍 Running: $script_name"
    echo "------------------------------------------"
    
    if python3 "$script_path" 2>&1; then
        echo "✅ Completed: $script_name"
    else
        echo "❌ Failed: $script_name"
    fi
    echo ""
}

# Parse argument
TASK=${1:-all}

case $TASK in
    competitor)
        run_script "competitor-monitor.py"
        ;;
    reviews)
        run_script "review-monitor.py"
        ;;
    content)
        run_script "content-research.py"
        ;;
    all)
        run_script "competitor-monitor.py"
        run_script "review-monitor.py"
        run_script "content-research.py"
        
        echo "=========================================="
        echo "  📊 All Tasks Complete!"
        echo "=========================================="
        echo ""
        echo "Generated files:"
        ls -lh "$DATA_DIR"/*.json "$DATA_DIR"/*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
        ;;
    *)
        echo "Usage: $0 [competitor|reviews|content|all]"
        echo ""
        echo "Options:"
        echo "  competitor  - Run competitor monitoring only"
        echo "  reviews     - Run review monitoring only"
        echo "  content     - Run content research only"
        echo "  all         - Run all tasks (default)"
        exit 1
        ;;
esac

echo ""
echo "Done!"
