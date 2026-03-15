# Corrections Log

## 2026-03-15 - Weekly Backup Error
- [17:02] BACKUP: GitHub Push Protection blocked backup due to exposed Atlassian API Token in self-improving/domains/trello.md
  Type: backup_error
  Error: GH013 - Repository rule violations, push declined due to secret scanning
  Lesson: Never store API credentials in plaintext in Git-tracked files. Use environment files in ~/.openclaw/.secrets/ and reference them instead.
  Fix: Removed plaintext credentials, replaced with reference to secrets file location, amended commit, and re-pushed successfully.

## 2026-03-15 - PageSpeed Performance Issues
- [00:36] PERFORMANCE: Burnaby page mobile LCP = 13.56s (target: <2.5s)
  Type: performance_issue
  Page: /appliance-repair-burnaby/
  Current Score: Mobile 66, Desktop 85
  Issues: LCP 13.56s, CLS 0.019
  Recommended Fix: Optimize hero image (likely oversized), lazy load below-fold images, fix layout shifts from late-loading elements
  
- [00:36] PERFORMANCE: Vancouver page mobile score 75 (target: >90)
  Type: performance_issue
  Page: /appliance-repair-vancouver/
  Current Score: Mobile 75, Desktop 77
  Issues: LCP 3.31s, CLS 0.005
  Recommended Fix: Compress/resize images, ensure font preloading, fix cumulative layout shift
  
- [00:36] PERFORMANCE: Refrigerator page mobile score 76 (target: >90)
  Type: performance_issue
  Page: /refrigerator-repair-vancouver/
  Current Score: Mobile 76, Desktop 98
  Issues: LCP 3.53s, CLS 0.004
  Recommended Fix: Same image optimization as Vancouver page, may share common template issues

- [00:36] PERFORMANCE: Homepage mobile score 89 (just under target)
  Type: performance_issue
  Page: /
  Current Score: Mobile 89, Desktop 96
  Issues: None critical, but mobile could improve to hit 90+ target
  Recommended Fix: Minor image optimization to push over 90 threshold

## 2026-03-09
- [03:38] Initial assumption: Small SEO project → Reality: Full agency-grade operation
  Type: project scope understanding
  Context: User provided comprehensive 800+ line SEO command file with 20+ specialized commands
  Lesson: Always ask for full context before assuming project scope. This is a serious SEO operation requiring full tool stack.
  Confirmed: yes

- [04:50] System deployed: Professional SEO automation fully activated for Evo Appliances
  Type: system deployment
  Context: Successfully deployed automated SEO system including:
          - Weekly SEO audits (cron)
          - Daily social media automation (3x/day via Postiz)
          - Google Business Profile daily posts
          - Server-side WordPress management
          - Created /appliance-repair-vancouver/ page (2000+ words)
  Lesson: Full-stack SEO automation is possible with proper API access and server credentials
  Confirmed: yes
