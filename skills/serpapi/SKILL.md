---
name: serpapi
description: "Google Search rank tracking via SerpAPI. Monitor keyword positions, track ranking changes, and get alerts when positions drop."
---

# SerpAPI Rank Tracking

Track Evo Appliances' Google rankings for target keywords.

## Setup

API Key stored in: `/root/.openclaw/.secrets/serpapi.env`

## Usage

### Check Single Keyword Ranking

```bash
# Check ranking for specific keyword
curl "https://serpapi.com/search?q=appliance+repair+vancouver&engine=google&location=Vancouver%2C+British+Columbia%2C+Canada&api_key=73ad159b9a2139640a783affd7435e156b57afa9f4e60926374d5345c71f925a"
```

### Track All Keywords

```python
import requests
import json
from datetime import datetime

API_KEY = "73ad159b9a2139640a783affd7435e156b57afa9f4e60926374d5345c71f925a"
KEYWORDS = [
    "appliance repair vancouver",
    "refrigerator repair vancouver",
    "washer repair vancouver",
    # ... more keywords
]

def check_ranking(keyword):
    """Check Google ranking for a keyword"""
    url = "https://serpapi.com/search"
    params = {
        "q": keyword,
        "engine": "google",
        "location": "Vancouver, British Columbia, Canada",
        "google_domain": "google.ca",
        "gl": "ca",
        "hl": "en",
        "api_key": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Find evoappliances.ca position
    position = None
    for i, result in enumerate(data.get('organic_results', []), 1):
        if 'evoappliances.ca' in result.get('link', ''):
            position = i
            break
    
    return {
        'keyword': keyword,
        'position': position,
        'date': datetime.now().isoformat()
    }
```

## SEO Use Cases

### 1. Daily Rank Monitoring
- Check top 10 keywords daily
- Log positions to track trends
- Alert if position drops >3 spots

### 2. Competitor Tracking
- Track where competitors rank
- Identify opportunities
- Monitor their content strategy

### 3. New Keyword Discovery
- Test new keywords before targeting
- Check search volume and competition
- Validate content ideas

### 4. Local SEO Tracking
- Track "near me" keywords
- Monitor Google Local Pack rankings
- Track service area keywords

## Cron Job Integration

```bash
# Daily rank check at 8 AM
0 8 * * * /usr/bin/python3 /root/.openclaw/workspace/skills/serpapi/track_ranks.py
```

## Alert Conditions

Send alert when:
- Ranking drops 3+ positions
- Falls off page 1 (position >10)
- Competitor overtakes you
- New keyword reaches page 1

## Data Storage

Rankings logged to:
`/root/.openclaw/workspace/rankings/YYYY-MM-DD.json`

## API Limits

- Free tier: 100 searches/month
- Current usage: ~300 searches/month (10 keywords × 30 days)
- May need upgrade for more keywords
