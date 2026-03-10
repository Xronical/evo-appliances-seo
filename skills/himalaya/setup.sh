#!/bin/bash
# Evo Appliances Email Setup Script
# Run this after configuring your email credentials

echo "=========================================="
echo "  📧 Evo Appliances Email Setup"
echo "=========================================="
echo ""

# Check if config exists
CONFIG_FILE="/root/.openclaw/.secrets/email.env"

if [ -f "$CONFIG_FILE" ]; then
    echo "✅ Email configuration found"
    source "$CONFIG_FILE"
    echo "   Email: $EMAIL_ADDRESS"
else
    echo "❌ Configuration not found"
    echo "   Please create: $CONFIG_FILE"
    echo ""
    echo "   Required format:"
    echo "   EMAIL_ADDRESS=your@email.com"
    echo "   EMAIL_PASSWORD=your-app-password"
    echo "   SMTP_HOST=smtp.gmail.com"
    echo "   SMTP_PORT=465"
    echo "   IMAP_HOST=imap.gmail.com"
    echo "   IMAP_PORT=993"
fi

echo ""
echo "=========================================="
echo "  📧 Testing Email Connection"
echo "=========================================="

# Run Python test
python3 /root/.openclaw/workspace/skills/himalaya/test_email.py 2>/dev/null || echo "Test script not found"
