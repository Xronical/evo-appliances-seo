---
name: content-refresh
description: "Automatically identify and refresh old blog posts. Update outdated content, add new information, and republish to boost SEO rankings."
---

# Content Refresh Automation

Keep your blog content fresh and ranking high by automatically updating old posts.

## Why Refresh Content?

- Google prefers fresh, updated content
- Old posts lose rankings over time
- Updated posts get a "freshness" boost
- Opportunity to add new keywords and internal links

## How It Works

### 1. Identify Old Posts
Scans WordPress for posts older than 6 months

### 2. Analyze Content
- Checks for outdated stats/info
- Identifies missing keywords
- Finds opportunities for new internal links

### 3. Auto-Update
- Adds "Updated: [Date]" notice
- Refreshes introduction and conclusion
- Adds new tips/sections where relevant
- Updates metadata

### 4. Republish
- Changes publish date to current
- Creates redirect from old URL (if slug changes)
- Submits to Google for re-indexing

### 5. Promote
- Creates social media post: "Updated guide: [Title]"
- Adds to email newsletter queue
- Updates Trello Content Calendar

## Configuration

### Posts to Refresh (Priority Order)
1. Posts older than 6 months with declining traffic
2. Posts ranking on page 2 (positions 11-20)
3. Posts with outdated information
4. Posts missing target keywords

### Refresh Rules
- **Max 2 posts per week** (don't overwhelm readers)
- **Keep original URL** (unless major restructure)
- **Preserve comments** (mark as "updated" instead of new)
- **Add "Last Updated" date** prominently

## Usage

### Manual Refresh
```bash
# Refresh specific post
python3 /root/.openclaw/workspace/skills/content-refresh/refresh_post.py --post-id=123

# Find posts needing refresh
python3 /root/.openclaw/workspace/skills/content-refresh/find_old_posts.py
```

### Automated Refresh
Weekly cron job identifies and refreshes 1-2 posts automatically.

## Content Refresh Checklist

When refreshing a post:
- [ ] Update publish date
- [ ] Add "Updated [Date]" notice
- [ ] Refresh introduction
- [ ] Check all facts/stats are current
- [ ] Add new keywords naturally
- [ ] Add 2-3 new internal links
- [ ] Update images if needed
- [ ] Refresh conclusion with new CTA
- [ ] Check all external links work
- [ ] Optimize meta description
- [ ] Create social media promotion

## SEO Benefits

- **Freshness signal** to Google
- **Improved rankings** for target keywords  
- **More internal links** = better site structure
- **Updated keywords** = capture new search trends
- **Better user experience** = lower bounce rate

## Integration

- **WordPress**: WP-CLI for post updates
- **Trello**: Track refresh status
- **Social Media**: Auto-promote updated content
- **Rank Tracking**: Monitor ranking improvements
