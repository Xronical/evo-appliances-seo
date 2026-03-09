---
name: notion
description: "Notion API for creating and managing pages, databases, and blocks. Use for SEO documentation, content planning, keyword research tracking, and SOPs."
---

# Notion Skill

Use the Notion API to manage pages, databases, and content programmatically.

## Setup

1. Create integration: https://www.notion.so/my-integrations
2. Get your Internal Integration Token
3. Share pages/databases with your integration

Set environment variable:
```bash
export NOTION_TOKEN="secret_xxxxxxxx"
```

## Common Tasks

### Create a Page
```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent": { "database_id": "DATABASE_ID" },
    "properties": {
      "Name": { "title": [{ "text": { "content": "SEO Strategy 2024" } }] }
    }
  }'
```

### Query a Database
```bash
curl -X POST "https://api.notion.com/v1/databases/DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28"
```

## SEO Use Cases

### 1. Keyword Research Database
- Properties: Keyword, Volume, Difficulty, Intent, Page Targeted, Status
- Track all keywords you're targeting

### 2. Content Calendar
- Properties: Title, Due Date, Status, Platform, Notes
- Plan blog posts, social media, GBP posts

### 3. Competitor Analysis
- Properties: Competitor, Domain Authority, Top Keywords, Notes
- Track what competitors are doing

### 4. SEO SOPs (Standard Operating Procedures)
- Create documented processes for:
  - On-page optimization
  - Content creation
  - Link building
  - Technical SEO checks

### 5. Monthly Reports
- Create structured pages for monthly SEO reports
- Include traffic, rankings, conversions

## Example: Create Keyword Database

```bash
curl -X POST "https://api.notion.com/v1/databases" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent": { "page_id": "PAGE_ID" },
    "title": [{ "type": "text", "text": { "content": "Evo Appliances - Keywords" } }],
    "properties": {
      "Keyword": { "title": {} },
      "Search Volume": { "number": {} },
      "Difficulty": { "select": { "options": [
        { "name": "Easy", "color": "green" },
        { "name": "Medium", "color": "yellow" },
        { "name": "Hard", "color": "red" }
      ]}},
      "Status": { "select": { "options": [
        { "name": "Researching", "color": "gray" },
        { "name": "Targeting", "color": "blue" },
        { "name": "Ranking", "color": "green" }
      ]}},
      "Current Position": { "number": {} }
    }
  }'
```
