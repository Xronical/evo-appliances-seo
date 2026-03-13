---
name: self-improving
description: "Custom self-improving system for Evo Appliances SEO automation. Captures learnings, corrections, and patterns to enable continuous improvement across all SEO tasks."
---

# Self-Improving Agent System

Custom self-improvement system optimized for Evo Appliances SEO automation.

## Overview

This skill enables the agent to:
- ✅ Learn from mistakes and corrections
- ✅ Remember user preferences automatically
- ✅ Apply patterns across similar tasks
- ✅ Improve quality over time without repetition
- ✅ Maintain continuity across sessions

## Architecture

### Memory Structure

```
~/self-improving/
├── memory.md              # Hot-tier preferences (load every session)
├── corrections.md         # Error log with lessons learned
├── reflections.md         # Periodic insights and observations
├── index.md              # Quick reference guide
├── domains/
│   └── seo.md            # SEO-specific patterns
└── projects/
    └── evo-appliances.md # Project-specific memory
```

### Memory Tiers

| Tier | Location | Load Frequency | Decay |
|------|----------|----------------|-------|
| HOT | memory.md | Every session | Never |
| WARM | corrections.md (recent) | Every session | 30 days |
| COLD | archive/ | On demand | 90 days |

## Usage

### Before Every Task

```bash
# Load hot-tier memory
read ~/self-improving/memory.md
read ~/self-improving/corrections.md (last 7 days)

# Check domain patterns
if task.type == "seo":
    read ~/self-improving/domains/seo.md
```

### After Errors/Corrections

```bash
# Log to corrections.md
echo "- [$(date)] $ERROR_DESCRIPTION
  Type: $ERROR_TYPE
  Context: $CONTEXT
  Lesson: $LESSON
  Confirmed: pending" >> ~/self-improving/corrections.md
```

### After Major Insights

```bash
# Add to memory.md if pattern confirmed 3+ times
if occurrence_count >= 3:
    append_to_memory_confirmed()
else:
    append_to_memory_active()
```

## Evo Appliances Context

### Company Profile
- **Business**: Appliance repair service
- **Location**: Vancouver, BC + Lower Mainland
- **Services**: Refrigerator, washer, dryer, dishwasher, oven/stove repair
- **USP**: Same-day service, all brands
- **Phone**: (604) 200-3054
- **Website**: https://evoappliances.ca

### SEO Priorities
1. Local SEO (Vancouver, Burnaby, Richmond, Surrey)
2. Service-specific keywords
3. Content marketing (blog posts)
4. Social media automation
5. Backlink building

### User Preferences (Confirmed)
- Keep meta descriptions under 160 characters
- Use phone number CTA in social posts
- Prioritize revenue-driving keywords over vanity metrics
- Maintain professional but approachable tone
- Weekly blog posts + daily social media

## Patterns

### SEO Patterns
- Title format: "[Service] [Location] | [Benefit] | Evo Appliances"
- Meta format: "[Benefit] in [Location]. [CTA]. Call (604) 200-3054"
- Content length: 800-1200 words for blogs
- Internal linking: Link to 2-3 related service pages

### Content Patterns
- Hook: Problem statement or question
- Body: Solution with actionable steps
- CTA: Phone number + booking link
- Social proof: Include reviews/testimonials

### Automation Patterns
- Cron jobs: Prefer isolated sessions
- API calls: Add delays for rate limits
- Error handling: Log and retry with backoff

## Integration

### With Cron Jobs
All 12 cron jobs should:
1. Load self-improving memory before execution
2. Log any errors to corrections.md
3. Report patterns observed

### With Skills
- Trello: Use for task tracking
- GitHub: Backup self-improving directory weekly
- SerpAPI: Log rate limit issues
- Postiz: Track successful posting patterns

## Maintenance

### Weekly
- Review corrections.md
- Confirm patterns that occurred 3+ times
- Archive old entries (>30 days)

### Monthly
- Update domain patterns
- Review project-specific learnings
- Consolidate redundant entries

### Quarterly
- Full memory audit
- Update SKILL.md with new patterns
- Archive cold-tier memory

## Commands

### Log Correction
```bash
log_correction() {
    local error="$1"
    local lesson="$2"
    echo "- [$(date '+%Y-%m-%d %H:%M')] $error
  Type: correction
  Lesson: $lesson
  Confirmed: pending" >> ~/self-improving/corrections.md
}
```

### Confirm Pattern
```bash
confirm_pattern() {
    local pattern="$1"
    if grep -q "$pattern" ~/self-improving/memory.md; then
        # Move from Active to Confirmed
        sed -i "s/## Active Patterns/## Confirmed Patterns/" ~/self-improving/memory.md
    fi
}
```

### Load Memory
```bash
load_memory() {
    cat ~/self-improving/memory.md
    cat ~/self-improving/corrections.md | tail -20
    cat ~/self-improving/domains/seo.md
}
```

## Error Recovery

### Context Loss
If session is compacted:
1. Read ~/self-improving/memory.md first
2. Read last 3 days of corrections
3. Ask user for any critical context

### Memory Corruption
1. Restore from GitHub backup
2. Rebuild from session history
3. Confirm key patterns with user

## Success Metrics

- Corrections repeated: <5%
- User corrections per session: Decreasing trend
- Pattern confirmations: Increasing trend
- Task completion rate: >95%

---
*Last updated: March 14, 2026*
*Version: 1.0*
*Maintained by: Evo Appliances SEO Agent*
