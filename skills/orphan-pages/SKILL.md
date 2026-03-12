---
name: orphan-pages
description: "Find and fix orphan pages on Evo Appliances website. Orphan pages have no incoming internal links, making them invisible to users and search engines."
---

# Orphan Pages Fixer

## What Are Orphan Pages?

Pages that exist on your website but have **no internal links** pointing to them. This means:
- ❌ Users can't find them by navigating
- ❌ Search engines may not discover them
- ❌ They get no link equity (SEO value)

## Current Orphan Pages (from Ahrefs)

1. https://evoappliances.ca/appliance-repair-kitsilano/ (0 internal links)
2. https://evoappliances.ca/appliance-repair-richmond/ (0 internal links)
3. https://evoappliances.ca/appliance-repair-vancouver/ (0 internal links)
4. https://evoappliances.ca/appliance-repair-burnaby/ (0 internal links)

## Solution

### 1. Add Links from Homepage
Create a "Service Areas" section on homepage linking to all location pages.

### 2. Add Footer Links
Add all service areas to the footer navigation.

### 3. Cross-Link Between Service Pages
Each location page should link to other nearby locations.

### 4. Add to Main Navigation
Add dropdown for "Service Areas" in main menu.

## Implementation

### Via WordPress SSH

```bash
# Get all pages
wp post list --post_type=page --format=json

# Find pages with no internal links (orphan detection)
# This requires crawling the site or using Ahrefs API

# Add internal links by editing content
wp post update PAGE_ID --post_content='NEW_CONTENT_WITH_LINKS'
```

## Automation

Weekly check:
1. Export all pages from WordPress
2. Crawl site to count internal links to each page
3. Identify pages with 0 internal links
4. Create Trello card to fix each orphan page
5. Add links from homepage or footer

## Why This Matters

- **SEO**: Orphan pages get no link equity
- **User Experience**: Users can't find these pages
- **Wasted Content**: You created pages that no one sees
- **Crawl Budget**: Google wastes time on pages it can't reach

## Prevention

- Always add new pages to navigation or link from existing pages
- Include location links in footer
- Create "Service Areas" hub page linking to all locations
- Regular monthly audit for orphan pages
