---
name: himalaya
description: "CLI email client for Evo Appliances. Send backlink outreach, check responses, and manage SEO communications via IMAP/SMTP."
---

# Himalaya Email Automation

Email CLI tool for Evo Appliances SEO outreach and communication.

## ✅ Status: CONNECTED

- **Email:** evoaappliances@gmail.com
- **Provider:** Gmail (IMAP/SMTP)
- **Version:** Himalaya v1.2.0

---

## Quick Commands

### Check Inbox
```bash
himalaya envelope list --page-size 10
```

### Read Email
```bash
himalaya envelope read 14800
```

### Write New Email
```bash
himalaya message write
# Opens editor, save and send
```

### Send Backlink Outreach (Template)
```bash
himalaya message write --to editor@site.com \
  --subject "Quick question about your site" \
  --body "Hi there, I came across your blog..."
```

### Search Emails
```bash
himalaya envelope list --filter "backlink OR outreach"
```

---

## Backlink Outreach Workflow

### Step 1: Prepare Contact List
Create a file with prospects from Trello:
```bash
# /tmp/prospects.txt
editor@vancouverhomeblog.com|Vancouver Home Blog|Sarah
contact@burnabydirectory.ca|Burnaby Business Directory|Team
info@homemaintenance.ca|Home Maintenance Tips|Editor
```

### Step 2: Send Bulk Outreach
```bash
while IFS='|' read -r email site name; do
  himalaya message write \
    --to "$email" \
    --subject "Quick question about $site" \
    --body "Hi $name, I came across $site and really appreciated your content..."
done < /tmp/prospects.txt
```

### Step 3: Track Responses
```bash
# Check for replies every few days
himalaya envelope list --filter "Re: Quick question" --page-size 20
```

---

## Email Templates

Templates stored in: `~/.config/himalaya/templates.toml`

### Available Templates:
1. **backlink-outreach** - Initial backlink request
2. **follow-up** - Follow-up email after no response
3. **client-report** - Monthly SEO report to clients

### Use Template:
```bash
# Himalaya doesn't have native template support yet
# Use the Python script instead:
python3 /root/.openclaw/workspace/skills/himalaya/evo_email.py
```

---

## SEO Use Cases

### 1. Automated Backlink Outreach
- Get prospects from Trello "🔍 Prospects" list
- Send personalized emails to each
- Move card to "📧 Contacted" after sending
- Track responses and update Trello

### 2. Client Communication
- Send monthly SEO reports
- Notify about ranking improvements
- Share new content published

### 3. Alert Monitoring
- Check Google Search Console emails
- Monitor for backlink responses
- Track competitor mentions

### 4. Email Digest
```bash
# Daily email summary
crontab -e
# Add: 0 9 * * * himalaya envelope list --page-size 5 > /tmp/daily_emails.txt
```

---

## Integration with Trello

### Auto-Send When Card Moves
When a card moves to "📧 Contacted" in Link Building board:
1. Extract email from card description
2. Send himalaya outreach email
3. Log sent email to card comment
4. Move card to "⏳ Waiting Response"

### Check Responses
Daily check:
```bash
himalaya envelope list --since yesterday | grep -i "re:"
```
For each response:
1. Find matching Trello card
2. Move to appropriate list
3. Add reply content as comment

---

## Security

- ✅ **App Password** used (not main Gmail password)
- ✅ Credentials in `~/.config/himalaya/config.toml`
- ✅ Config file NOT backed up to GitHub
- ✅ Gmail 2FA enabled (required for App Passwords)

---

## Rate Limiting (Important!)

To avoid Gmail spam filters:
- **Max 20 emails/hour** for outreach
- **Max 100 emails/day** total
- Space out bulk sends by 2-3 minutes
- Warm up: Start with 5-10 emails/day, increase gradually

---

## Troubleshooting

### "Authentication failed"
```bash
# Check config
cat ~/.config/himalaya/config.toml
# Verify App Password is correct (not your Gmail password)
```

### "Connection refused"
```bash
# Check if IMAP is enabled in Gmail
# https://mail.google.com/mail/u/0/#settings/fwdandpop
# Enable IMAP access
```

### "Cannot parse config"
```bash
# Validate TOML syntax
source $HOME/.cargo/env
himalaya --debug account list
```

---

## Configuration File

Location: `~/.config/himalaya/config.toml`

```toml
[accounts.gmail]
default = true
email = "evoaappliances@gmail.com"
display-name = "Evo Appliances"

[accounts.gmail.backend]
type = "imap"
host = "imap.gmail.com"
port = 993
login = "evoaappliances@gmail.com"

[accounts.gmail.backend.auth]
type = "password"
cmd = "echo 'YOUR_APP_PASSWORD'"

[accounts.gmail.sender]
type = "smtp"
host = "smtp.gmail.com"
port = 465
login = "evoaappliances@gmail.com"

[accounts.gmail.sender.auth]
type = "password"
cmd = "echo 'YOUR_APP_PASSWORD'"

signature = "--\nEvo Appliances | Vancouver Appliance Repair\n📞 (604) 200-3054 | 🌐 https://evoappliances.ca"
```

---

## Related

- **Trello Skill** - Track outreach prospects
- **Python Script** - `/root/.openclaw/workspace/skills/himalaya/evo_email.py`
- **Backup Script** - `/root/.openclaw/workspace/skills/himalaya/setup.sh`
