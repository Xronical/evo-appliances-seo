#!/usr/bin/env python3
"""
Scrapling Integration with Proxy Rotation for Evo Appliances SEO
Content research - find trending appliance repair topics
"""

from scrapling.fetchers import Fetcher, StealthyFetcher
from scrapling.parser import Selector
import json
from datetime import datetime
import time
import random

# Proxy configuration - add paid proxies here for better results
PAID_PROXIES = [
    None,  # Direct connection
    # "http://user:pass@proxy1.example.com:8080",
]

def get_proxy():
    """Get a random proxy"""
    return random.choice(PAID_PROXIES)

def scrape_with_proxy(url: str, selector: str, name: str) -> list:
    """Scrape with proxy rotation and multiple strategies"""
    print(f"🔍 Scraping {name}...")
    
    ideas = []
    
    # Try different approaches with and without proxy
    approaches = [
        {"type": "stealth", "proxy": None},
        {"type": "stealth", "proxy": get_proxy()},
        {"type": "fetcher", "impersonate": "chrome", "proxy": None},
        {"type": "fetcher", "impersonate": "firefox", "proxy": get_proxy()},
    ]
    
    for i, approach in enumerate(approaches):
        try:
            print(f"  Attempt {i+1} ({approach['type']}, proxy={approach['proxy'] is not None})...")
            
            if approach["type"] == "stealth":
                page = StealthyFetcher.fetch(
                    url,
                    headless=True,
                    network_idle=True,
                    google_search=False
                )
            else:
                proxy = approach.get("proxy")
                if proxy:
                    page = Fetcher.get(url, impersonate=approach["impersonate"], proxy=proxy)
                else:
                    page = Fetcher.get(url, impersonate=approach["impersonate"])
            
            elements = page.css(selector)
            
            for elem in elements[:15]:
                title = elem.css('::text').get('').strip()
                link = elem.css('a::attr(href)').get('') or url
                
                if title and len(title) > 10:
                    ideas.append({
                        "title": title,
                        "source": name,
                        "source_url": url,
                        "link": link if link.startswith('http') else f"{url}/{link.lstrip('/')}",
                        "suggested_blog_title": f"{title} - Vancouver Appliance Repair Guide",
                        "method": f"attempt_{i+1}"
                    })
            
            if ideas:
                print(f"  ✅ Found {len(ideas)} ideas on attempt {i+1}")
                return ideas
                
        except Exception as e:
            print(f"  ⚠️  Attempt {i+1} failed: {str(e)[:80]}")
            time.sleep(1)
            continue
    
    print(f"  ❌ All attempts failed")
    return ideas

def scrape_google_trends():
    """Find trending appliance topics via Google searches"""
    print("🔍 Finding trending appliance topics...")
    
    search_queries = [
        "most common refrigerator problems 2024",
        "washing machine won't spin fix",
        "dryer not heating repair tips",
        "dishwasher leaking how to fix",
        "oven not heating repair cost",
        "freezer frost buildup fix"
    ]
    
    all_ideas = []
    
    for query in search_queries:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        try:
            proxy = get_proxy()
            if proxy:
                page = Fetcher.get(search_url, impersonate='chrome', proxy=proxy)
            else:
                page = StealthyFetcher.fetch(search_url, headless=True, network_idle=True)
            
            # Get "People also ask" questions
            questions = page.css('[data-attrid="wa:/description"], .related-question-pair, div[jsname="Cpkphb"]')
            
            for q in questions[:5]:
                question = q.css('::text').get('').strip()
                if question and len(question) > 10 and '?' in question:
                    all_ideas.append({
                        "title": question,
                        "source": "Google People Also Ask",
                        "search_query": query,
                        "suggested_blog_title": f"{question} - Expert Vancouver Appliance Repair Tips"
                    })
            
            # Get related searches
            related = page.css('a[href*="/search?q="]')
            for r in related[:5]:
                text = r.css('::text').get('').strip()
                if text and len(text) > 10 and text not in [i['title'] for i in all_ideas]:
                    all_ideas.append({
                        "title": text,
                        "source": "Google Related Searches",
                        "search_query": query,
                        "suggested_blog_title": f"{text} - Vancouver Appliance Repair Guide"
                    })
            
        except Exception as e:
            print(f"  ⚠️  Search '{query[:30]}...' failed: {str(e)[:60]}")
            continue
    
    # Remove duplicates
    seen = set()
    unique_ideas = []
    for idea in all_ideas:
        if idea["title"] not in seen:
            seen.add(idea["title"])
            unique_ideas.append(idea)
    
    return unique_ideas[:20]  # Return top 20

def generate_content_calendar(ideas: list) -> dict:
    """Generate a weekly content calendar from ideas"""
    calendar = {
        "generated_at": datetime.now().isoformat(),
        "weeks": []
    }
    
    for i in range(0, len(ideas), 4):
        week_ideas = ideas[i:i+4]
        week = {
            "week_number": (i // 4) + 1,
            "posts": week_ideas
        }
        calendar["weeks"].append(week)
    
    return calendar

def main():
    print("=" * 60)
    print("  Evo Appliances - Content Research with Proxy Rotation")
    print("=" * 60)
    print()
    
    all_ideas = []
    
    # Google Trends research (most reliable)
    print("📚 PHASE 1: Google Search Research")
    print("-" * 60)
    
    google_ideas = scrape_google_trends()
    all_ideas.extend(google_ideas)
    print(f"  ✅ Found {len(google_ideas)} ideas from Google searches")
    
    # Alternative sources
    print()
    print("🔍 PHASE 2: Alternative Sources")
    print("-" * 60)
    
    # Try DIY Stack Exchange
    diy_ideas = scrape_with_proxy(
        "https://diy.stackexchange.com/questions/tagged/appliance",
        ".question-summary .summary h3",
        "DIY Stack Exchange"
    )
    all_ideas.extend(diy_ideas)
    
    # Generate calendar
    calendar = generate_content_calendar(all_ideas)
    
    # Save results
    import os
    data_dir = "/root/.openclaw/workspace/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Save all ideas
    ideas_file = f"{data_dir}/content-ideas.json"
    with open(ideas_file, 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_ideas": len(all_ideas),
            "ideas": all_ideas
        }, f, indent=2)
    
    # Save calendar
    calendar_file = f"{data_dir}/content-calendar.json"
    with open(calendar_file, 'w') as f:
        json.dump(calendar, f, indent=2)
    
    # Generate report
    report_lines = [
        "# Content Ideas Report",
        f"Generated: {datetime.now().isoformat()}",
        f"Total Ideas: {len(all_ideas)}",
        "",
        "## Top Content Ideas",
        ""
    ]
    
    for i, idea in enumerate(all_ideas[:15], 1):
        report_lines.append(f"### {i}. {idea['title']}")
        report_lines.append(f"- **Source:** {idea.get('source', 'Unknown')}")
        report_lines.append(f"- **Suggested Blog Title:** {idea.get('suggested_blog_title', '')}")
        if "search_query" in idea:
            report_lines.append(f"- **Search Query:** {idea['search_query']}")
        report_lines.append("")
    
    report_file = f"{data_dir}/content-ideas-report.md"
    with open(report_file, 'w') as f:
        f.write("\n".join(report_lines))
    
    print()
    print("=" * 60)
    print(f"✅ Ideas JSON: {ideas_file}")
    print(f"✅ Calendar JSON: {calendar_file}")
    print(f"✅ Report: {report_file}")
    print("=" * 60)
    print()
    print(f"📊 Total content ideas found: {len(all_ideas)}")
    print(f"📅 Generated calendar for: {len(calendar['weeks'])} weeks")
    
    if all_ideas:
        print("\n📝 Top 5 Ideas:")
        for i, idea in enumerate(all_ideas[:5], 1):
            print(f"  {i}. {idea['title'][:70]}...")

if __name__ == "__main__":
    main()
