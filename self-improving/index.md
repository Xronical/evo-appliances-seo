# Self-Improving Index

## Quick Reference

### Load Memory Before Tasks
```bash
source ~/self-improving/load_memory.sh
# OR
read ~/self-improving/memory.md
```

### Log Correction
1. Edit `~/self-improving/corrections.md`
2. Add entry with format:
```
- [YYYY-MM-DD HH:MM] Description
  Type: correction|insight|pattern
  Context: What happened
  Lesson: What to do differently
  Confirmed: pending
```

### Confirm Pattern
After 3+ occurrences, move from "Active Patterns" to "Confirmed Preferences"

### Files Location
| File | Purpose |
|------|---------|
| memory.md | Hot-tier preferences |
| corrections.md | Error log |
| reflections.md | Periodic insights |
| domains/seo.md | SEO-specific patterns |
| projects/evo-appliances.md | Project context |

## Common Tasks

### Before SEO Task
```
read ~/self-improving/memory.md
read ~/self-improving/domains/seo.md
```

### Before Social Media Post
```
read ~/self-improving/memory.md (check posting preferences)
```

### After Error
```
append to corrections.md
if error repeated 3x: add to memory.md
```

## Active Patterns to Watch

1. **Meta description length** - User corrects if >160 chars
2. **Page title length** - User corrects if >60 chars
3. **Rate limit handling** - Always add delays for SerpAPI
4. **Verification** - Always verify posts actually published

## Skills Integration

- **Trello**: Log tasks from corrections
- **GitHub**: Backup this directory weekly
- **Cron**: Load memory before each job

---
*Quick reference for self-improving system*
