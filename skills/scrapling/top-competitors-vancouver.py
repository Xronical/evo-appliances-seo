#!/usr/bin/env python3
"""
Scrapling Integration - Top Rated Vancouver Appliance Repair Competitors
Scrapes top competitors from Google, Yelp, and their websites
"""

from scrapling.fetchers import Fetcher, StealthyFetcher
from scrapling.parser import Selector
import json
import re
from datetime import datetime

# Top Vancouver Appliance Repair Competitors to Monitor
TOP_COMPETITORS = {
    "vancouver-appliance-repair": {
        "name": "Vancouver Appliance Repair",
        "url": "https://www.vancouverappliancerepair.ca/",
        "yelp_url": "https://www.yelp.com/biz/vancouver-appliance-repair-vancouver-2",
        "search_term": "Vancouver Appliance Repair"
    },
    "appliance-repair-vancouver": {
        "name": "Appliance Repair Vancouver",
        "url": "https://www.appliancerepairvancouver.ca/",
        "yelp_url": "https://www.yelp.com/biz/appliance-repair-vancouver-vancouver",
        "search_term": "Appliance Repair Vancouver"
    },
    "appliance-service-master": {
        "name": "Appliance Service Master",
        "url": "https://www.applianceservicemaster.ca/",
        "search_term": "Appliance Service Master Vancouver"
    },
    "surrey-appliance-repair": {
        "name": "Surrey Appliance Repair",
        "url": "https://www.surreyappliancerepair.ca/",
        "search_term": "Surrey Appliance Repair"
    },
    "burnaby-appliance-repair": {
        "name": "Burnaby Appliance Repair",
        "url": "https://www.burnabyappliancerepair.ca/",
        "search_term": "Burnaby Appliance Repair"
    }
}

def scrape_google_reviews(search_term: str) -> dict:
    """Scrape Google reviews and ratings for a competitor"""
    print(f"🔍 Searching Google for: {search_term}")
    
    try:
        search_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}+reviews"
        page = StealthyFetcher.fetch(search_url, headless=True, network_idle=True)
        
        data = {
            "search_term": search_term,
            "scraped_at": datetime.now().isoformat(),
            "rating": None,
            "review_count": None,
            "highlights": []
        }
        
        # Try to extract rating
        rating_text = page.css('[data-attrid="kc:/local:lu.attribute.rating"]::text').get('')
        if not rating_text:
            rating_text = page.css('span:contains("stars")::text').get('')
        
        if rating_text:
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            if rating_match:
                data["rating"] = float(rating_match.group(1))
        
        # Try to extract review count
        review_text = page.css('[data-attrid="kc:/local:lu.attribute.review_count"]::text').get('')
        if review_text:
            review_match = re.search(r'(\d+)', review_text.replace(',', ''))
            if review_match:
                data["review_count"] = int(review_match.group(1))
        
        # Extract review highlights
        highlights = page.css('[data-attrid="kc:/local:lu.attribute.highlights"] .JjtOXd, .y0WAac')
        for h in highlights[:5]:
            text = h.css('::text').get('').strip()
            if text and len(text) > 5:
                data["highlights"].append(text)
        
        return data
        
    except Exception as e:
        print(f"  ⚠️  Google search failed: {str(e)[:80]}")
        return {
            "search_term": search_term,
            "error": str(e)[:100],
            "scraped_at": datetime.now().isoformat()
        }

def scrape_website_intel(url: str, name: str) -> dict:
    """Scrape competitor website for services, pricing, and SEO data"""
    print(f"🔍 Scraping website: {name}")
    
    data = {
        "name": name,
        "url": url,
        "scraped_at": datetime.now().isoformat(),
        "page_title": "",
        "meta_description": "",
        "services": [],
        "pricing_mentions": [],
        "contact_info": {},
        "headings": [],
        "service_areas": []
    }
    
    try:
        # Try multiple approaches
        approaches = [
            lambda: StealthyFetcher.fetch(url, headless=True, network_idle=True),
            lambda: Fetcher.get(url, impersonate='chrome'),
            lambda: Fetcher.get(url, impersonate='firefox')
        ]
        
        page = None
        for i, approach in enumerate(approaches):
            try:
                print(f"  Attempt {i+1}...")
                page = approach()
                break
            except Exception as e:
                print(f"    Attempt {i+1} failed: {str(e)[:60]}")
                continue
        
        if not page:
            data["error"] = "All connection attempts failed"
            return data
        
        # Page title
        data["page_title"] = page.css('title::text').get('').strip()
        
        # Meta description
        data["meta_description"] = page.css('meta[name="description"]::attr(content)').get('')
        
        # Extract all headings (H1, H2, H3)
        for level in ['h1', 'h2', 'h3']:
            headings = page.css(f'{level}::text').getall()
            for h in headings[:10]:
                h_clean = h.strip()
                if h_clean and len(h_clean) > 3:
                    data["headings"].append({
                        "level": level.upper(),
                        "text": h_clean
                    })
        
        # Extract services from common selectors
        service_selectors = [
            '.service', '.service-item', '[class*="service"]',
            '.offer', '.offering', '[class*="offer"]',
            '[class*="appliance"]', '.elementor-widget-heading'
        ]
        
        for selector in service_selectors:
            elements = page.css(selector)
            for elem in elements[:15]:
                text = elem.css('::text').get('').strip()
                if text and 5 < len(text) < 100:
                    if text not in data["services"]:
                        data["services"].append(text)
            if len(data["services"]) >= 8:
                break
        
        # Extract pricing mentions
        price_selectors = ['[class*="price"]', '[class*="cost"]', '[class*="rate"]']
        for selector in price_selectors:
            elements = page.css(selector)
            for elem in elements[:5]:
                text = elem.css('::text').get('').strip()
                if text and '$' in text and len(text) < 50:
                    data["pricing_mentions"].append(text)
        
        # Extract contact info
        phone = page.css('[href^="tel:"]::attr(href)').get('')
        email = page.css('[href^="mailto:"]::attr(href)').get('')
        if phone:
            data["contact_info"]["phone"] = phone.replace('tel:', '')
        if email:
            data["contact_info"]["email"] = email.replace('mailto:', '')
        
        # Look for service areas/locations
        location_keywords = ['vancouver', 'burnaby', 'richmond', 'surrey', 'north vancouver', 'coquitlam']
        body_text = ' '.join(page.css('body::text').getall()).lower()
        for location in location_keywords:
            if location in body_text:
                data["service_areas"].append(location.title())
        data["service_areas"] = list(set(data["service_areas"]))  # Remove duplicates
        
        print(f"  ✅ Found {len(data['services'])} services, {len(data['headings'])} headings")
        return data
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
        data["error"] = str(e)[:100]
        return data

def scrape_yelp_data(yelp_url: str, name: str) -> dict:
    """Scrape Yelp reviews and ratings"""
    print(f"🔍 Checking Yelp: {name}")
    
    data = {
        "name": name,
        "yelp_url": yelp_url,
        "scraped_at": datetime.now().isoformat(),
        "rating": None,
        "review_count": None,
        "top_reviews": []
    }
    
    try:
        page = StealthyFetcher.fetch(yelp_url, headless=True, network_idle=True)
        
        # Try to extract rating
        rating_elem = page.css('[aria-label*="star"], .i-stars__09f24__M1AR7')
        if rating_elem:
            aria_label = rating_elem.css('::attr(aria-label)').get('')
            rating_match = re.search(r'(\d+\.?\d*)', aria_label)
            if rating_match:
                data["rating"] = float(rating_match.group(1))
        
        # Try to extract review count
        review_elem = page.css('a[href*="reviews"]:contains("review")')
        if review_elem:
            review_text = review_elem.css('::text').get('')
            review_match = re.search(r'(\d+)', review_text.replace(',', ''))
            if review_match:
                data["review_count"] = int(review_match.group(1))
        
        # Extract top review snippets
        reviews = page.css('.raw__09f24__T4Ezm, .comment__09f24__D0cxf')
        for r in reviews[:5]:
            text = r.css('::text').get('').strip()
            if text and len(text) > 20:
                data["top_reviews"].append(text[:200])
        
        print(f"  ✅ Yelp rating: {data['rating']}, Reviews: {data['review_count']}")
        return data
        
    except Exception as e:
        print(f"  ⚠️  Yelp scrape failed: {str(e)[:80]}")
        data["error"] = str(e)[:100]
        return data

def generate_competitor_report(data: dict) -> str:
    """Generate a markdown report from competitor data"""
    report = []
    report.append("# Vancouver Appliance Repair - Competitor Intelligence Report")
    report.append(f"Generated: {data['scraped_at']}")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    
    # Find best rated competitor
    ratings = []
    for comp in data.get('competitors', []):
        if 'google_data' in comp and comp['google_data'].get('rating'):
            ratings.append((comp['name'], comp['google_data']['rating'], comp['google_data'].get('review_count', 0)))
    
    if ratings:
        ratings.sort(key=lambda x: x[1], reverse=True)
        report.append(f"**Top Rated Competitor:** {ratings[0][0]} ({ratings[0][1]}★, {ratings[0][2]} reviews)")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Detailed competitor analysis
    for comp in data.get('competitors', []):
        report.append(f"## {comp['name']}")
        report.append("")
        
        # Google data
        if 'google_data' in comp and not comp['google_data'].get('error'):
            gd = comp['google_data']
            report.append(f"### Google Profile")
            if gd.get('rating'):
                report.append(f"- **Rating:** {gd['rating']}/5")
            if gd.get('review_count'):
                report.append(f"- **Reviews:** {gd['review_count']}")
            if gd.get('highlights'):
                report.append(f"- **Highlights:** {', '.join(gd['highlights'][:3])}")
            report.append("")
        
        # Website data
        if 'website_data' in comp and not comp['website_data'].get('error'):
            wd = comp['website_data']
            report.append(f"### Website Analysis")
            report.append(f"- **URL:** {wd['url']}")
            if wd.get('page_title'):
                report.append(f"- **Title:** {wd['page_title'][:80]}")
            if wd.get('services'):
                report.append(f"- **Services:** {len(wd['services'])} found")
                for s in wd['services'][:5]:
                    report.append(f"  - {s}")
            if wd.get('service_areas'):
                report.append(f"- **Service Areas:** {', '.join(wd['service_areas'])}")
            if wd.get('pricing_mentions'):
                report.append(f"- **Pricing:** {wd['pricing_mentions'][0]}")
            report.append("")
        
        # Yelp data
        if 'yelp_data' in comp and comp['yelp_data'] and not comp['yelp_data'].get('error'):
            yd = comp['yelp_data']
            if yd.get('rating') or yd.get('review_count'):
                report.append(f"### Yelp Profile")
                if yd.get('rating'):
                    report.append(f"- **Rating:** {yd['rating']}/5")
                if yd.get('review_count'):
                    report.append(f"- **Reviews:** {yd['review_count']}")
                report.append("")
        
        report.append("---")
        report.append("")
    
    # Recommendations
    report.append("## Recommendations for Evo Appliances")
    report.append("")
    report.append("Based on competitor analysis:")
    report.append("")
    report.append("1. **Service Offerings:** Ensure all major appliance types are clearly listed")
    report.append("2. **Service Areas:** Expand visibility for all Vancouver-area locations")
    report.append("3. **Pricing:** Consider adding pricing guidance or service call fees")
    report.append("4. **Reviews:** Focus on Google Business Profile review generation")
    report.append("5. **SEO:** Target the same service keywords as top competitors")
    report.append("")
    
    return "\n".join(report)

def main():
    print("=" * 70)
    print("  Evo Appliances - TOP RATED Competitor Intelligence (Vancouver)")
    print("=" * 70)
    print()
    
    all_competitor_data = []
    
    for key, competitor in TOP_COMPETITORS.items():
        print(f"📊 Analyzing: {competitor['name']}")
        print("-" * 70)
        
        comp_data = {
            "key": key,
            "name": competitor['name'],
            "scraped_at": datetime.now().isoformat()
        }
        
        # Scrape Google data
        print("  → Google Search...")
        comp_data["google_data"] = scrape_google_reviews(competitor['search_term'])
        
        # Scrape website
        print("  → Website...")
        comp_data["website_data"] = scrape_website_intel(competitor['url'], competitor['name'])
        
        # Scrape Yelp if available
        if 'yelp_url' in competitor:
            print("  → Yelp...")
            comp_data["yelp_data"] = scrape_yelp_data(competitor['yelp_url'], competitor['name'])
        
        all_competitor_data.append(comp_data)
        print()
    
    # Compile final data
    output = {
        "scraped_at": datetime.now().isoformat(),
        "target_location": "Vancouver, BC",
        "competitors_analyzed": len(TOP_COMPETITORS),
        "competitors": all_competitor_data
    }
    
    # Save JSON
    import os
    data_dir = "/root/.openclaw/workspace/data"
    os.makedirs(data_dir, exist_ok=True)
    
    json_file = f"{data_dir}/top-competitors-vancouver.json"
    with open(json_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Generate report
    report = generate_competitor_report(output)
    report_file = f"{data_dir}/top-competitors-report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print("=" * 70)
    print("✅ COMPETITOR ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    print(f"📁 JSON Data: {json_file}")
    print(f"📄 Report: {report_file}")
    print()
    
    # Summary
    print("📊 Summary:")
    for comp in all_competitor_data:
        name = comp['name']
        rating = comp.get('google_data', {}).get('rating', 'N/A')
        reviews = comp.get('google_data', {}).get('review_count', 'N/A')
        services = len(comp.get('website_data', {}).get('services', []))
        print(f"  • {name}: {rating}★ ({reviews} reviews) | {services} services found")

if __name__ == "__main__":
    main()
