# Trello Integration Patterns

## Evo Appliances Trello Boards

### Board 1: Content Calendar
- **Purpose**: Manage blog post pipeline
- **Lists**: Ideas → In Progress → Review → Published

### Board 2: Link Building
- **Purpose**: Track backlink outreach
- **Lists**: Prospects → Contacted → Responded → Links Secured

### Board 3: SEO Tasks
- **Purpose**: Technical SEO task management
- **Lists**: Backlog → To Do → In Progress → Done

## API Credentials
- Key: Stored in ~/.openclaw/.secrets/trello.env (KEY)
- Token: Stored in ~/.openclaw/.secrets/trello.env (TOKEN)

## Common Operations

### Get Boards
```bash
curl "https://api.trello.com/1/members/me/boards?key=KEY&token=TOKEN"
```

### Get Lists
```bash
curl "https://api.trello.com/1/boards/BOARD_ID/lists?key=KEY&token=TOKEN"
```

### Get Cards
```bash
curl "https://api.trello.com/1/lists/LIST_ID/cards?key=KEY&token=TOKEN"
```

### Create Card
```bash
curl -X POST "https://api.trello.com/1/cards" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "KEY",
    "token": "TOKEN",
    "idList": "LIST_ID",
    "name": "Card Title",
    "desc": "Card description"
  }'
```

## Card Format Standards

**SEO Task Card:**
```
Name: Fix: [Brief Issue Description]
Desc: Priority: High/Medium/Low
     Issue: [Detailed description]
     Pages affected: [X]
     Recommended action: [Steps]
Due: Based on priority (High=1 week, Medium=2 weeks, Low=1 month)
```

**Backlink Prospect Card:**
```
Name: Site: [domain.com]
Desc: DR: [X] | Contact: [email] | Notes: [notes]
```

## Lessons Learned

- Always verify board/list IDs before creating cards
- Use consistent naming conventions for searchability
- Set due dates based on priority levels
