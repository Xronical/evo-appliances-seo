#!/usr/bin/env python3
"""
Scrapling Integration for Evo Appliances SEO
Review monitoring script - tracks Google/Yelp reviews
"""

from scrapling.fetchers import StealthyFetcher
import json
import re
from datetime import datetime

# Business profiles to monitor
BUSINESSES = {
    "evo-appliances-google": {
        "name": "Evo Appliances Google Profile",
        "type": "google",
        # Note: Google Business Profile requires special handling
        # This is a placeholder for the CID
        "cid": "YOUR_GOOGLE_CID_HERE"
    },
    "competitor-1": {
        "name": "Appliance Repair Vancouver",
        "type": "yelp",
        "url": "https://www.yelp.com/biz/appliance-repair-vancouver"
    }
}

def scrape_yelp_reviews(business_url: str, business_name: str) -> dict:
    """Scrape Yelp reviews for a business"""
    print(f"🔍 Scraping Yelp reviews for {business_name}...")
    
    try:
        # Yelp blocks bots, use stealth mode
        page = StealthyFetcher.fetch(
            business_url, 
            headless=True,
            network_idle=True,
            google_search=False  # Avoid Google redirect
        )
        
        reviews = []
        
        # Extract review elements
        review_elements = page.css('.review, [data-testid="review"]')
        
        for elem in review_elements[:20]:  # First 20 reviews
            review_data = {
                "text": "",
                "rating": 0,
                "date": "",
                "author": ""
            }
            
            # Review text
            text_elem = elem.css('.raw__09f24__T4Ezm, .comment__09f24__D0cxf')
            if text_elem:
                review_data["text"] = text_elem.css('::text').get('').strip()[:500]
            
            # Rating
            rating_elem = elem.css('[aria-label*="star"], .i-stars__09f24__M1AR7')
            if rating_elem:
                aria_label = rating_elem.css('::attr(aria-label)').get('')
                rating_match = re.search(r'(\d+\.?\d*)', aria_label)
                if rating_match:
                    review_data["rating"] = float(rating_match.group(1))
            
            # Date
            date_elem = elem.css('.css-chan6m, [class*="date"]')
            if date_elem:
                review_data["date"] = date_elem.css('::text').get('').strip()
            
            # Author
            author_elem = elem.css('.css-1p9ibgf, [class*="user-name"]')
            if author_elem:
                review_data["author"] = author_elem.css('::text').get('').strip()
            
            if review_data["text"]:
                reviews.append(review_data)
        
        # Calculate average rating
        ratings = [r["rating"] for r in reviews if r["rating"] > 0]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        return {
            "business_name": business_name,
            "source": "yelp",
            "url": business_url,
            "scraped_at": datetime.now().isoformat(),
            "total_reviews_found": len(reviews),
            "average_rating": round(avg_rating, 2),
            "reviews": reviews
        }
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {
            "business_name": business_name,
            "source": "yelp",
            "error": str(e),
            "scraped_at": datetime.now().isoformat()
        }

def generate_review_report(data: dict) -> str:
    """Generate a summary report from review data"""
    report = []
    report.append("# Review Monitoring Report")
    report.append(f"Generated: {data['scraped_at']}")
    report.append("")
    
    for business in data.get('businesses', []):
        report.append(f"## {business['business_name']}")
        report.append(f"- Source: {business['source']}")
        report.append(f"- Reviews Found: {business.get('total_reviews_found', 0)}")
        report.append(f"- Average Rating: {business.get('average_rating', 0)}/5")
        report.append("")
        
        # Recent reviews
        report.append("### Recent Reviews:")
        for review in business.get('reviews', [])[:5]:
            report.append(f"- **{review.get('rating', 'N/A')}★** ({review.get('date', 'Unknown')})")
            report.append(f"  {review.get('text', 'No text')[:150]}...")
            report.append("")
    
    return "\n".join(report)

def main():
    print("=" * 60)
    print("  Evo Appliances - Review Monitoring (Scrapling)")
    print("=" * 60)
    print()
    
    results = {
        "scraped_at": datetime.now().isoformat(),
        "businesses": []
    }
    
    # Scrape each business
    for key, business in BUSINESSES.items():
        if business["type"] == "yelp" and "url" in business:
            data = scrape_yelp_reviews(business["url"], business["name"])
            results["businesses"].append(data)
        elif business["type"] == "google":
            print(f"⚠️  Google Business Profile requires API access - skipping {business['name']}")
    
    # Save JSON data
    import os
    data_dir = "/root/.openclaw/workspace/data"
    os.makedirs(data_dir, exist_ok=True)
    
    json_file = f"{data_dir}/reviews-monitor.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate markdown report
    report = generate_review_report(results)
    report_file = f"{data_dir}/reviews-report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print()
    print("=" * 60)
    print(f"✅ JSON data: {json_file}")
    print(f"✅ Report: {report_file}")
    print("=" * 60)
    print()
    print("📊 Summary:")
    for business in results["businesses"]:
        print(f"  {business['business_name']}: {business.get('total_reviews_found', 0)} reviews")

if __name__ == "__main__":
    main()
