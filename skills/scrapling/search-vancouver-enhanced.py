#!/usr/bin/env python3
"""
Scrapling Integration - Search "appliance repair Vancouver" with better extraction
"""

from scrapling.fetchers import Fetcher, StealthyFetcher
from scrapling.parser import Selector
import json
import re
from datetime import datetime
import time

def search_with_stealth(query: str) -> dict:
    """Search Google with multiple stealth approaches"""
    print(f"🔍 Searching: {query}")
    
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    data = {
        "query": query,
        "scraped_at": datetime.now().isoformat(),
        "organic_results": [],
        "people_also_ask": [],
        "related_searches": [],
        "local_businesses": []
    }
    
    try:
        # Try stealth fetcher
        page = StealthyFetcher.fetch(
            search_url, 
            headless=True, 
            network_idle=True,
            google_search=False
        )
        
        # Wait a bit for content to load
        time.sleep(2)
        
        # Get page source for debugging
        html_content = page.css('html').get('')
        
        # Try multiple selectors for search results
        result_selectors = [
            'div.g',
            'div[data-hveid]',
            'div[jscontroller]',
            '.g',
            '[data-ved]'
        ]
        
        for selector in result_selectors:
            results = page.css(selector)
            print(f"  Selector '{selector}': Found {len(results)} elements")
            
            for elem in results[:5]:
                # Try to find title
                title = None
                for title_sel in ['h3', '.LC20lb', 'a h3', '[role="heading"]']:
                    title = elem.css(f'{title_sel}::text').get('').strip()
                    if title and len(title) > 5:
                        break
                
                # Try to find URL
                url = elem.css('a::attr(href)').get('')
                
                # Try to find snippet
                snippet = elem.css('div span::text, .VwiC3b::text').get('')
                
                if title and url and 'google' not in url and len(title) > 10:
                    # Check if not already added
                    if not any(r['title'] == title for r in data["organic_results"]):
                        data["organic_results"].append({
                            "title": title[:100],
                            "url": url[:200],
                            "snippet": snippet[:300] if snippet else ''
                        })
            
            if len(data["organic_results"]) >= 5:
                break
        
        # Extract "People also ask"
        paa_selectors = [
            '[data-attrid="wa:/description"]',
            '.related-question-pair',
            'div[jsname="Cpkphb"]',
            'div[role="button"]'
        ]
        
        for selector in paa_selectors:
            questions = page.css(selector)
            for q in questions:
                text = q.css('::text').get('').strip()
                if text and '?' in text and len(text) > 15:
                    if text not in data["people_also_ask"]:
                        data["people_also_ask"].append(text)
        
        # Extract related searches
        related = page.css('a[href*="/search?q="]')
        for r in related:
            text = r.css('::text').get('').strip()
            if text and len(text) > 10 and text not in data["related_searches"]:
                data["related_searches"].append(text)
        
        return data
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:150]}")
        data["error"] = str(e)[:200]
        return data

def main():
    print("=" * 70)
    print("  Scrapling - Enhanced Appliance Repair Vancouver Search")
    print("=" * 70)
    print()
    
    # Main search
    search_data = search_with_stealth("appliance repair Vancouver")
    
    print()
    print(f"📊 Results:")
    print(f"  • Organic results: {len(search_data['organic_results'])}")
    print(f"  • 'People also ask': {len(search_data['people_also_ask'])}")
    print(f"  • Related searches: {len(search_data['related_searches'])}")
    print()
    
    # Show what we found
    if search_data['organic_results']:
        print("🌐 Top Organic Results:")
        for i, r in enumerate(search_data['organic_results'][:5], 1):
            print(f"  {i}. {r['title'][:60]}...")
    
    if search_data['people_also_ask']:
        print("\n❓ People Also Ask:")
        for q in search_data['people_also_ask'][:8]:
            print(f"  • {q[:80]}")
    
    # Save data
    import os
    data_dir = "/root/.openclaw/workspace/data"
    os.makedirs(data_dir, exist_ok=True)
    
    output = {
        "scraped_at": datetime.now().isoformat(),
        "search_query": "appliance repair Vancouver",
        "results": search_data
    }
    
    json_file = f"{data_dir}/vancouver-search-enhanced.json"
    with open(json_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Generate simple report
    report = f"""# Appliance Repair Vancouver - Search Data
Generated: {datetime.now().isoformat()}

## Search Query
`appliance repair Vancouver`

## Results Summary
- Organic results: {len(search_data['organic_results'])}
- People also ask: {len(search_data['people_also_ask'])}
- Related searches: {len(search_data['related_searches'])}

## People Also Ask (Content Ideas)
"""
    
    for i, q in enumerate(search_data['people_also_ask'], 1):
        report += f"{i}. {q}\n"
    
    if search_data['organic_results']:
        report += "\n## Top Search Results\n"
        for i, r in enumerate(search_data['organic_results'][:10], 1):
            report += f"\n### {i}. {r['title']}\n"
            report += f"- URL: {r['url']}\n"
            if r['snippet']:
                report += f"- Snippet: {r['snippet'][:150]}...\n"
    
    report_file = f"{data_dir}/vancouver-search-enhanced.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print()
    print("=" * 70)
    print(f"✅ Data saved to: {json_file}")
    print(f"✅ Report saved to: {report_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
