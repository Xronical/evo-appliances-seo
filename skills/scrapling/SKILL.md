# Scrapling Skill

## Overview

Scrapling integration for Evo Appliances SEO automation. Provides web scraping capabilities for competitor monitoring, review tracking, and content research.

## Location

`/root/.openclaw/workspace/skills/scrapling/`

## Scripts

### 1. competitor-monitor.py
**Purpose:** Monitor competitor websites for services, pricing, and SEO data.

**Usage:**
```bash
python3 /root/.openclaw/workspace/skills/scrapling/competitor-monitor.py
```

**Output:**
- `/root/.openclaw/workspace/data/competitor-intel.json`

**What it scrapes:**
- Competitor service listings
- Pricing information
- Contact details
- Meta descriptions (SEO analysis)

### 2. review-monitor.py
**Purpose:** Monitor Yelp and other review sites for competitor/customer reviews.

**Usage:**
```bash
python3 /root/.openclaw/workspace/skills/scrapling/review-monitor.py
```

**Output:**
- `/root/.openclaw/workspace/data/reviews-monitor.json`
- `/root/.openclaw/workspace/data/reviews-report.md`

**What it tracks:**
- Review ratings
- Review text
- Review dates
- Average ratings

### 3. content-research.py
**Purpose:** Find content ideas from industry blogs and Reddit.

**Usage:**
```bash
python3 /root/.openclaw/workspace/skills/scrapling/content-research.py
```

**Output:**
- `/root/.openclaw/workspace/data/content-ideas.json`
- `/root/.openclaw/workspace/data/content-calendar.json`
- `/root/.openclaw/workspace/data/content-ideas-report.md`

**What it finds:**
- Trending appliance repair topics
- Common customer questions
- Blog post ideas with Vancouver angles

## Features

- **Stealth Mode:** Bypasses Cloudflare and anti-bot detection
- **Adaptive Parsing:** Automatically adjusts to website changes
- **Concurrent Requests:** Fast parallel scraping
- **JSON Export:** Easy integration with other tools

## Cron Jobs

Weekly competitor monitoring:
```
Schedule: 0 7 * * TUE (Tuesdays 7 AM)
Script: /root/.openclaw/workspace/skills/scrapling/competitor-monitor.py
```

## Dependencies

- Python 3.10+
- scrapling
- playwright
- curl_cffi

## Notes

- Always respect robots.txt
- Use responsibly for competitor research only
- Some sites may block scraping - use stealth mode
