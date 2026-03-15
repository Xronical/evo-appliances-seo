# Self-Improving Memory

## Confirmed Preferences
<!-- Patterns confirmed by user, never decay -->

### SEO Meta Descriptions
- **Length**: Maximum 160 characters
- **Format**: Include primary keyword + location + phone CTA
- **Example**: "Same-day appliance repair in Vancouver. Expert service for all brands. Call Evo Appliances (604) 200-3054."
- **Phone**: Always include (604) 200-3054

### Page Titles
- **Length**: Maximum 60 characters
- **Format**: [Service] [Location] | [Benefit] | Evo Appliances
- **Separator**: Use pipe (|) not dash (-)

### Social Media Posts
- **Frequency**: 3x daily (8am, 2pm, 6pm PST)
- **Content**: Mix of tips, promotions, and helpful info
- **CTA**: Always include phone (604) 200-3054
- **Images**: Use Pixabay, resize for Instagram (4:5 ratio)

### API Rate Limits
- **SerpAPI**: 100 searches/month on free tier
- **Workaround**: Add 5-second delays between searches
- **Alternative**: Reduce to 3 keywords or upgrade to paid

### Postiz Social Posting
- **Status**: Subscription renewed, working
- **Platforms**: Facebook, Instagram, X, LinkedIn, GBP
- **Check**: Always verify posts actually published

### WordPress Integration
- **Access**: SSH via WP-CLI
- **Credentials**: Stored in ~/.openclaw/.secrets/server.env
- **Path**: /home/rinnt515/public_html

### Intelligence Gathering (Primary Tools)
**PRIMARY - Brave Search API:**
- **API Key:** BSAE1mTB9-QjjjDFTuy_kkVJeUwjVDK
- **Purpose:** Competitor intelligence, content research, backlink opportunities
- **Schedule:** Tuesdays 7 AM (weekly)
- **Status:** Working reliably, no blocking issues
- **Best for:** Finding competitor mentions, industry news, directory opportunities

**PRIMARY - SerpAPI:**
- **API Key:** 73ad159b9a2139640a783affd7435e156b57afa9f4e60926374d5345c71f925a
- **Purpose:** Google rank tracking for 12 keywords
- **Schedule:** Daily 8 AM
- **Limitations:** 100 searches/month free tier (rate limited)
- **Workaround:** 5-second delays between searches
- **Status:** Functional but may need upgrade for daily use

**SECONDARY - Scrapling Web Scraping:**
- **Status:** Limited success due to anti-bot blocking
- **Use for:** Specific unprotected sites only
- **Schedule:** Disabled - use manually when needed
- **Note:** Many sites (Google, Yelp, Reddit) block scraping - use APIs instead

### Automation Schedule
- **Daily**: Social media (3x), GBP post, rank tracking
- **Weekly**: SEO audit, speed test, blog post, backlink outreach
- **Monthly**: Orphan page check, content refresh

### Content Preferences
- **Blog length**: 800-1200 words
- **Tone**: Professional but approachable
- **Focus**: Local SEO for Vancouver + Lower Mainland
- **Keywords**: appliance repair vancouver, refrigerator repair, etc.

### Error Handling
- **Log all errors** to corrections.md
- **Retry with backoff** for rate limits
- **Verify** before marking as complete

## Active Patterns
<!-- Patterns observed 3+ times, subject to decay -->

- User corrects meta descriptions that are too long
- User prefers Option A/B/C choices presented clearly
- User wants immediate fixes when issues found
- User tracks all changes in GitHub

## Recent (last 7 days)
<!-- New corrections pending confirmation -->

- 2026-03-13: SerpAPI rate limit hit due to rapid-fire requests (no delays)
  Solution: Add 5-second delays between keyword checks
  
- 2026-03-13: Postiz subscription expired, posts failing silently
  Solution: Renewed subscription, verified working
  
- 2026-03-13: Page titles too long (>60 chars)
  Solution: Shortened all service area page titles

- 2026-03-15: Scrapling web scraping limited by anti-bot protection
  Decision: Use Brave Search API and SerpAPI as primary intelligence tools
  Scrapling moved to secondary/backup role for specific unprotected sites only

## Evo Appliances Context
- **Business**: Appliance repair service
- **Location**: Vancouver, BC + Lower Mainland (Burnaby, Richmond, Surrey, etc.)
- **Services**: Refrigerator, washer, dryer, dishwasher, oven/stove repair
- **USP**: Same-day service, all brands, licensed technicians
- **Phone**: (604) 200-3054
- **Website**: https://evoappliances.ca
- **SEO Goal**: Revenue-driving local traffic, not vanity metrics
- **Tone**: Helpful, trustworthy, expert, local, conversion-focused

### Target Keywords
- Primary: "appliance repair vancouver"
- Secondary: "refrigerator repair vancouver", "washer repair vancouver", "dryer repair vancouver"
- Local: "appliance repair burnaby", "appliance repair richmond", "appliance repair surrey"

### Active Campaigns
- Daily social media (3x/day via Postiz)
- Daily GBP posts
- Weekly blog posts
- Weekly backlink outreach
- Daily rank tracking (currently rate-limited)

### Blog Post Archive (2026)

| Date | Title | URL | Word Count | Topic |
|------|-------|-----|------------|-------|
| Mar 15 | 5 Essential Refrigerator Maintenance Tips Every Vancouver Homeowner Should Know | https://evoappliances.ca/5-essential-refrigerator-maintenance-tips-every-vancouver-homeowner-should-know/ | 1,006 | Refrigerator Maintenance |

### Content Performance Learnings
- **Topic**: Refrigerator maintenance performs well (high search volume + local relevance)
- **Format**: Numbered tips with H2 headings + bullet lists = easy to scan
- **Length**: ~1,000 words strikes good balance (comprehensive but not overwhelming)
- **CTA**: Phone number + URL in conclusion drives conversions
- **SSH Publishing**: Working with sshpass for automated WP-CLI deployment

---
*Last updated: March 15, 2026*
