---
name: himalaya
description: "CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language)."
---

# Himalaya Email CLI

Use the `himalaya` CLI to manage emails from the terminal.

## Quick Start

List emails in inbox:
```bash
himalaya list
```

Read an email:
```bash
himalaya read 123
```

Write a new email:
```bash
himalaya write
```

## Common Tasks

### Search Emails
```bash
himalaya search "from:example.com"
```

### Reply to Email
```bash
himalaya reply 123
```

### Forward Email
```bash
himalaya forward 123
```

### Delete Email
```bash
himalaya delete 123
```

## SEO Use Cases

- **Backlink Outreach**: Send personalized emails to bloggers
- **Client Communication**: Manage SEO client emails
- **Alert Monitoring**: Check Google Search Console alert emails
- **Newsletter Management**: Organize industry newsletters

## Configuration

Himalaya uses a TOML config file at `~/.config/himalaya/config.toml`:

```toml
[account]
default = "gmail"

[account.gmail]
email = "your@gmail.com"
imap-host = "imap.gmail.com"
imap-port = 993
smtp-host = "smtp.gmail.com"
smtp-port = 465
```

For Gmail, use an App Password (not your regular password).
