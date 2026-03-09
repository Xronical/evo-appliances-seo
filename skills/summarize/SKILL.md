---
name: summarize
description: "Summarize or extract text/transcripts from URLs, podcasts, and local files. Great fallback for transcribing YouTube/video or summarizing competitor content."
---

# Summarize Skill

Use the `summarize` CLI to extract and summarize content from URLs, podcasts, videos, and files.

## Installation

```bash
npm install -g summarize-cli
```

## Quick Start

### Summarize a URL
```bash
summarize https://example.com/article
```

### Summarize with specific length
```bash
summarize https://example.com/article --length short
# Options: short, medium, long
```

### Extract transcript from YouTube
```bash
summarize https://youtube.com/watch?v=VIDEO_ID --transcript
```

### Summarize a podcast
```bash
summarize https://podcast-url.com/episode --transcript
```

### Process local file
```bash
summarize ./document.pdf
summarize ./audio.mp3 --transcript
```

## SEO Use Cases

### 1. Competitor Content Analysis
```bash
# Summarize top-ranking competitor articles
summarize https://competitor.com/appliance-repair-guide --length medium
```

### 2. Video Content to Blog Posts
```bash
# Extract transcript from YouTube video
summarize https://youtube.com/watch?v=appliance-tips --transcript > blog-post.md
```

### 3. Research Aggregation
```bash
# Summarize multiple sources for research
summarize https://site1.com/article https://site2.com/article --combined
```

### 4. Podcast to Social Media
```bash
# Get key points from podcast for social posts
summarize https://podcast.com/seo-tips --length short --key-points
```

### 5. PDF Reports
```bash
# Extract key insights from PDF reports
summarize ./industry-report.pdf --length medium
```

## Advanced Options

```bash
# Get bullet points
summarize URL --format bullets

# Get key quotes
summarize URL --quotes

# Extract entities (people, companies, etc.)
summarize URL --entities

# Specify output format
summarize URL --output markdown
summarize URL --output json
```

## Example Workflow

```bash
# 1. Find competitor content
# 2. Summarize it
summarize https://competitor.com/top-article --length medium > summary.txt

# 3. Identify content gaps
# 4. Create better content for Evo Appliances
```
