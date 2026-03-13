#!/bin/bash
# Self-Improving System Loader
# Source this before any task to load relevant memory

echo "🧠 Loading self-improving memory..."

# Hot-tier (always load)
if [ -f ~/self-improving/memory.md ]; then
    echo ""
    echo "=== CONFIRMED PREFERENCES ==="
    grep -A2 "## Confirmed Preferences" ~/self-improving/memory.md | tail -5
fi

# Recent corrections (last 7 days)
if [ -f ~/self-improving/corrections.md ]; then
    echo ""
    echo "=== RECENT CORRECTIONS ==="
    tail -20 ~/self-improving/corrections.md
fi

# Domain-specific
if [ -f ~/self-improving/domains/seo.md ]; then
    echo ""
    echo "=== SEO DOMAIN PATTERNS ==="
    grep "###" ~/self-improving/domains/seo.md | head -5
fi

# Project-specific
if [ -f ~/self-improving/projects/evo-appliances.md ]; then
    echo ""
    echo "=== EVO APPLIANCES CONTEXT ==="
    head -15 ~/self-improving/projects/evo-appliances.md
fi

echo ""
echo "✅ Memory loaded. Ready to execute with context."
