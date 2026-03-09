---
name: trello
description: "Manage Trello boards, lists, and cards via the Trello REST API. Create boards for SEO projects, track tasks, manage content calendars, and organize link building outreach."
---

# Trello Skill

Use the Trello REST API to manage boards, lists, and cards programmatically.

## Setup

Get your API key and token from: https://trello.com/app-key

Set environment variables:
```bash
export TRELLO_API_KEY="your-api-key"
export TRELLO_TOKEN="your-token"
```

## Common Tasks

### Create a Board
```bash
curl -X POST "https://api.trello.com/1/boards/" \
  -d "name=SEO%20Project%20-Evo%20Appliances" \
  -d "key=$TRELLO_API_KEY" \
  -d "token=$TRELLO_TOKEN"
```

### Create a List
```bash
curl -X POST "https://api.trello.com/1/lists" \
  -d "name=Backlog" \
  -d "idBoard=BOARD_ID" \
  -d "key=$TRELLO_API_KEY" \
  -d "token=$TRELLO_TOKEN"
```

### Create a Card
```bash
curl -X POST "https://api.trello.com/1/cards" \
  -d "name=Create%20Burnaby%20landing%20page" \
  -d "desc=Write%202000%20words%20optimized%20for%20Burnaby" \
  -d "idList=LIST_ID" \
  -d "key=$TRELLO_API_KEY" \
  -d "token=$TRELLO_TOKEN"
```

## SEO Board Templates

### Content Calendar Board
- Lists: Ideas → Writing → Editing → Published → Promoted
- Cards: Each blog post or page

### Link Building Board
- Lists: Prospects → Contacted → In Progress → Links Live
- Cards: Each website for outreach

### Keyword Tracking Board
- Lists: Targeting → Optimizing → Ranking → Page 1
- Cards: Each keyword with position tracking

## Use Cases

1. **Track SEO Tasks**: Create cards for each optimization task
2. **Content Calendar**: Plan blog posts and social media
3. **Link Building**: Manage outreach campaigns
4. **Competitor Analysis**: Track competitor activities
