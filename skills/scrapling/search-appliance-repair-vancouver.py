#!/usr/bin/env python3
"""
Scrapling Integration - Search "appliance repair Vancouver" and extract data
"""

from scrapling.fetchers import Fetcher, StealthyFetcher
from scrapling.parser import Selector
import json
import re
from datetime import datetime

def search_google(query: str) -> dict:
    """Search Google and extract results"""
    print(f"🔍 Searching Google: {query}")
    
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    try:
        page = StealthyFetcher.fetch(search_url, headless=True, network_idle=True)
        
        data = {
            "query": query,
            "scraped_at": datetime.now().isoformat(),
            "organic_results": [],
            "local_results": [],
            "related_searches": [],
            "people_also_ask": []
        }
        
        # Extract organic search results
        results = page.css('div.g, div[data-ved]')
        
        for result in results[:10]:
            title_elem = result.css('h3')
            title = title_elem.css('::text').get('').strip()
            url = result.css('a::attr(href)').get('')
            snippet = result.css('div.VwiC3b::text, span[jsname="ktMZb"]::text').get('')
            
            if title and url and 'google.com' not in url:
                # Try to extract rating if present
                rating_text = result.css('span:contains("·")::text').get('')
                rating = None
                reviews = None
                
                if rating_text:
                    rating_match = re.search(r'(\d+\.\d+)', rating_text)
                    if rating_match:
                        rating = float(rating_match.group(1))
                    review_match = re.search(r'\((\d+)\)', rating_text)
                    if review_match:
                        reviews = int(review_match.group(1))
                
                data["organic_results"].append({
                    "title": title,
                    "url": url,
                    "snippet": snippet[:300] if snippet else '',
                    "rating": rating,
                    "review_count": reviews
                })
        
        # Extract "People also ask" questions
        paa_questions = page.css('[data-attrid="wa:/description"], .related-question-pair')
        for q in paa_questions[:8]:
            question = q.css('::text').get('').strip()
            if question and len(question) > 10 and '?' in question:
                data["people_also_ask"].append(question)
        
        # Extract related searches
        related = page.css('a[href*="/search?q="]')
        for r in related[:10]:
            text = r.css('::text').get('').strip()
            if text and len(text) > 10 and text not in [i for i in data["related_searches"]]:
                data["related_searches"].append(text)
        
        return data
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
        return {
            "query": query,
            "error": str(e)[:200],
            "scraped_at": datetime.now().isoformat()
        }

def scrape_business_website(url: str, name: str) -> dict:
    """Scrape a competitor's business website"""
    print(f"  📄 Scraping: {name[:50]}...")
    
    try:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
        
        data = {
            "name": name,
            "url": url,
            "title": page.css('title::text').get('').strip(),
            "meta_description": page.css('meta[name="description"]::attr(content)').get(''),
            "phone": None,
            "services": [],
            "headings": []
        }
        
        # Extract phone number
        phone = page.css('[href^="tel:"]::attr(href)').get('')
        if phone:
            data["phone"] = phone.replace('tel:', '')
        
        # Extract headings (indicates content structure)
        for h in page.css('h1, h2, h3'):
            text = h.css('::text').get('').strip()
            if text and len(text) > 3:
                data["headings"].append(text)
        
        # Look for service mentions
        service_keywords = ['refrigerator', 'washer', 'dryer', 'dishwasher', 'oven', 'stove', 'repair', 'installation']
        body_text = ' '.join(page.css('body ::text').getall()).lower()
        
        for keyword in service_keywords:
            if keyword in body_text:
                data["services"].append(keyword)
        
        data["services"] = list(set(data["services"]))
        
        return data
        
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "error": str(e)[:100]
        }

def main():
    print("=" * 70)
    print("  Scrapling - Appliance Repair Vancouver Search")
    print("=" * 70)
    print()
    
    # Main search
    search_data = search_google("appliance repair Vancouver")
    
    print()
    print(f"✅ Found {len(search_data.get('organic_results', []))} organic results")
    print(f"✅ Found {len(search_data.get('people_also_ask', []))} 'People also ask' questions")
    print(f"✅ Found {len(search_data.get('related_searches', []))} related searches")
    print()
    
    # Scrape top 3 business websites
    print("📄 Scraping top business websites...")
    print("-" * 70)
    
    business_data = []
    for result in search_data.get('organic_results', [])[:3]:
        if result.get('url'):
            website_data = scrape_business_website(result['url'], result['title'])
            business_data.append(website_data)
            
            if website_data.get('title'):
                print(f"  ✅ {website_data['title'][:50]}")
                print(f"     Phone: {website_data.get('phone', 'N/A')}")
                print(f"     Services: {', '.join(website_data.get('services', [])[:5])}")
    
    # Compile all data
    output = {
        "scraped_at": datetime.now().isoformat(),
        "search_query": "appliance repair Vancouver",
        "location": "Vancouver, BC",
        "search_results": search_data,
        "business_details": business_data
    }
    
    # Save to file
    import os
    data_dir = "/root/.openclaw/workspace/data"
    os.makedirs(data_dir, exist_ok=True)
    
    json_file = f"{data_dir}/appliance-repair-vancouver-search.json"
    with open(json_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Generate report
    report_lines = [
        "# Appliance Repair Vancouver - Search Results",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "## Top Search Results",
        ""
    ]
    
    for i, result in enumerate(search_data.get('organic_results', [])[:10], 1):
        report_lines.append(f"### {i}. {result['title']}")
        report_lines.append(f"- **URL:** {result['url']}")
        if result.get('snippet'):
            report_lines.append(f"- **Description:** {result['snippet'][:200]}")
        if result.get('rating'):
            report_lines.append(f"- **Rating:** {result['rating']}★ ({result.get('review_count', 'N/A')} reviews)")
        report_lines.append("")
    
    report_lines.extend([
        "## People Also Ask",
        ""
    ])
    
    for q in search_data.get('people_also_ask', []):
        report_lines.append(f"- {q}")
    
    report_lines.extend([
        "",
        "## Related Searches",
        ""
    ])
    
    for r in search_data.get('related_searches', [])[:15]:
        report_lines.append(f"- {r}")
    
    report_lines.extend([
        "",
        "## Business Details (Top 3)",
        ""
    ])
    
    for biz in business_data:
        if biz.get('title'):
            report_lines.append(f"### {biz['title']}")
            report_lines.append(f"- URL: {biz['url']}")
            if biz.get('phone'):
                report_lines.append(f"- Phone: {biz['phone']}")
            if biz.get('services'):
                report_lines.append(f"- Services: {', '.join(biz['services'][:5])}")
            report_lines.append("")
    
    report_file = f"{data_dir}/appliance-repair-vancouver-search.md"
    with open(report_file, 'w') as f:
        f.write('\n'.join(report_lines))
    
    print()
    print("=" * 70)
    print("✅ SEARCH COMPLETE")
    print("=" * 70)
    print()
    print(f"📁 JSON Data: {json_file}")
    print(f"📄 Report: {report_file}")
    print()
    print("📊 Summary:")
    print(f"  • Organic results: {len(search_data.get('organic_results', []))}")
    print(f"  • 'People also ask': {len(search_data.get('people_also_ask', []))}")
    print(f"  • Related searches: {len(search_data.get('related_searches', []))}")
    print(f"  • Websites scraped: {len([b for b in business_data if b.get('title')])}")

if __name__ == "__main__":
    main()
