#!/bin/bash
# Google APIs Master Script - Run both GA4 and Search Console data pulls

echo "=========================================="
echo "  Evo Appliances - Google APIs Data Pull"
echo "=========================================="
echo ""

SCRIPT_DIR="/root/.openclaw/workspace/skills/google-apis"
DATA_DIR="/root/.openclaw/workspace/data"

mkdir -p "$DATA_DIR"

echo "📊 Running Search Console data pull..."
echo "------------------------------------------"
python3 "$SCRIPT_DIR/search-console-pull.py"
echo ""

echo "📈 Running GA4 data pull..."
echo "------------------------------------------"
python3 "$SCRIPT_DIR/ga4-pull.py"
echo ""

echo "=========================================="
echo "  ✅ All Google API Data Pulled!"
echo "=========================================="
echo ""
echo "Generated files:"
ls -lh "$DATA_DIR"/*-data.json "$DATA_DIR"/*-report.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "Done!"
