#!/usr/bin/env python3
"""
Scrapling Integration with Proxy Rotation for Evo Appliances SEO
Competitor monitoring and data extraction script
"""

from scrapling.fetchers import Fetcher, StealthyFetcher
from scrapling.parser import Selector
import json
import sys
import random
from datetime import datetime

# Proxy configuration
# For production use, add your paid proxies here:
# Format: "http://user:pass@host:port" or "http://host:port"
# Recommended services: BrightData, Oxylabs, Smartproxy, PacketStream
PAID_PROXIES = [
    None,  # Direct connection (no proxy)
    # Add your paid proxies here:
    # "http://user:pass@proxy1.example.com:8080",
    # "http://user:pass@proxy2.example.com:8080",
]

def get_proxy():
    """Get a proxy from the list"""
    return random.choice(PAID_PROXIES)

def scrape_competitor_services(url: str, name: str) -> dict:
    """Scrape services and pricing from competitor websites with proxy rotation"""
    print(f"🔍 Scraping {name}...")
    
    data = {
        "name": name,
        "url": url,
        "scraped_at": datetime.now().isoformat(),
        "services": [],
        "pricing": [],
        "contact_info": {},
        "page_title": "",
        "meta_description": "",
        "attempts": []
    }
    
    # Try with different configurations
    attempts = [
        {"proxy": None, "impersonate": "chrome"},
        {"proxy": None, "impersonate": "firefox"},
        {"proxy": get_proxy(), "impersonate": "chrome"},
    ]
    
    for i, config in enumerate(attempts):
        attempt_info = {
            "attempt": i + 1,
            "proxy": "yes" if config["proxy"] else "no",
            "impersonate": config["impersonate"],
            "status": "failed"
        }
        
        try:
            print(f"  Attempt {i+1}: proxy={config['proxy'] is not None}, impersonate={config['impersonate']}")
            
            if config["proxy"]:
                # Use Fetcher with proxy
                page = Fetcher.get(
                    url, 
                    impersonate=config["impersonate"],
                    proxy=config["proxy"]
                )
            else:
                # Use StealthyFetcher without proxy
                page = StealthyFetcher.fetch(
                    url, 
                    headless=True,
                    network_idle=True,
                    google_search=False
                )
            
            # Extract page title
            data["page_title"] = page.css('title::text').get('').strip()
            
            # Extract services (try multiple selectors)
            service_selectors = [
                '.service', '.service-item', '[class*="service"]',
                '.offer', '.offering', '[class*="offer"]',
                'h2', 'h3', '.elementor-heading-title'
            ]
            
            for selector in service_selectors:
                elements = page.css(selector)
                for elem in elements[:15]:
                    service_text = elem.css('::text').get('').strip()
                    if service_text and 3 < len(service_text) < 100:
                        if service_text not in data["services"]:
                            data["services"].append(service_text)
                if len(data["services"]) >= 5:
                    break
            
            # Extract pricing mentions
            price_selectors = ['[class*="price"]', '[class*="cost"]', '.pricing']
            for selector in price_selectors:
                elements = page.css(selector)
                for elem in elements[:5]:
                    price_text = elem.css('::text').get('').strip()
                    if price_text and '$' in price_text and len(price_text) < 50:
                        data["pricing"].append(price_text)
            
            # Extract contact info
            phone = page.css('[href^="tel:"]::attr(href)').get('')
            email = page.css('[href^="mailto:"]::attr(href)').get('')
            if phone:
                data["contact_info"]["phone"] = phone.replace('tel:', '')
            if email:
                data["contact_info"]["email"] = email.replace('mailto:', '')
            
            # Extract meta description
            meta_desc = page.css('meta[name="description"]::attr(content)').get('')
            if meta_desc:
                data["meta_description"] = meta_desc
            
            attempt_info["status"] = "success"
            attempt_info["services_found"] = len(data["services"])
            data["attempts"].append(attempt_info)
            
            print(f"  ✅ Success! Found {len(data['services'])} services")
            return data
            
        except Exception as e:
            attempt_info["error"] = str(e)[:100]
            data["attempts"].append(attempt_info)
            print(f"  ⚠️  Attempt {i+1} failed: {str(e)[:80]}")
            continue
    
    # All attempts failed
    data["error"] = "All scraping attempts failed"
    return data

def scrape_directory_listings(city: str) -> list:
    """Scrape local business directories for backlink opportunities"""
    print(f"🔍 Finding directories in {city}...")
    
    search_queries = [
        f"{city} business directory appliance repair",
        f"{city} home services directory"
    ]
    
    all_directories = []
    
    for query in search_queries[:2]:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        try:
            page = StealthyFetcher.fetch(
                search_url, 
                headless=True, 
                network_idle=True,
                google_search=False
            )
            
            directories = []
            results = page.css('div.g, div[data-ved]')
            
            for result in results[:10]:
                title = result.css('h3::text').get('')
                url = result.css('a::attr(href)').get('')
                snippet = result.css('div.VwiC3b::text').get('')
                
                if title and url:
                    keywords = ['directory', 'list', 'guide', 'best', 'top']
                    if any(kw in title.lower() for kw in keywords):
                        directories.append({
                            "title": title,
                            "url": url,
                            "snippet": snippet[:200] if snippet else '',
                            "search_query": query
                        })
            
            all_directories.extend(directories)
            
        except Exception as e:
            print(f"  ⚠️  Search failed: {str(e)[:80]}")
            continue
    
    # Remove duplicates
    seen = set()
    unique_dirs = []
    for d in all_directories:
        if d["url"] not in seen:
            seen.add(d["url"])
            unique_dirs.append(d)
    
    return unique_dirs[:10]

def main():
    print("=" * 60)
    print("  Evo Appliances - Scrapling with Proxy Rotation")
    print("=" * 60)
    print()
    
    # Competitors to monitor
    COMPETITORS = {
        "appliance-repair-vancouver": "https://www.appliancerepairvancouver.ca/",
        "vancouver-appliance-repair": "https://www.vancouverappliancerepair.ca/",
        "surrey-appliance-repair": "https://www.surreyappliancerepair.ca/",
    }
    
    print("📊 PHASE 1: Competitor Analysis")
    print("-" * 60)
    
    competitor_data = []
    for name, url in COMPETITORS.items():
        data = scrape_competitor_services(url, name)
        competitor_data.append(data)
        if "error" in data and len(data.get("services", [])) == 0:
            print(f"  ❌ {name}: Failed after all attempts")
        else:
            print(f"  ✅ {name}: {len(data.get('services', []))} services")
    
    print()
    print("📁 PHASE 2: Directory Research")
    print("-" * 60)
    
    directories = scrape_directory_listings("Vancouver")
    print(f"  ✅ Found {len(directories)} potential directories")
    for d in directories[:5]:
        print(f"    • {d['title'][:50]}")
    
    # Save results
    output = {
        "scraped_at": datetime.now().isoformat(),
        "competitors": competitor_data,
        "directories": directories
    }
    
    output_file = "/root/.openclaw/workspace/data/competitor-intel.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print()
    print("=" * 60)
    print(f"✅ Results saved to: {output_file}")
    print("=" * 60)
    print()
    print("📊 Summary:")
    success_count = sum(1 for c in competitor_data if len(c.get("services", [])) > 0)
    print(f"  Successful scrapes: {success_count}/{len(COMPETITORS)}")
    print(f"  Directories found: {len(directories)}")

if __name__ == "__main__":
    main()
