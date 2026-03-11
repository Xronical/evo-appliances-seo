#!/usr/bin/env python3
"""
Evo Appliances Rank Tracking
Monitors Google rankings for target keywords
"""

import requests
import json
import os
from datetime import datetime

# Configuration
API_KEY = "73ad159b9a2139640a783affd7435e156b57afa9f4e60926374d5345c71f925a"
TARGET_DOMAIN = "evoappliances.ca"

KEYWORDS = [
    "appliance repair vancouver",
    "refrigerator repair vancouver",
    "washer repair vancouver",
    "dryer repair vancouver",
    "dishwasher repair vancouver",
    "appliance repair burnaby",
    "fridge repair vancouver",
    "washing machine repair vancouver",
    "oven repair vancouver",
    "stove repair vancouver",
    "appliance repair richmond",
    "refrigerator repair burnaby"
]

def check_ranking(keyword):
    """Check Google ranking for a keyword"""
    url = "https://serpapi.com/search"
    params = {
        "q": keyword,
        "engine": "google",
        "location": "Vancouver, British Columbia, Canada",
        "google_domain": "google.ca",
        "gl": "ca",
        "hl": "en",
        "num": 20,  # Get top 20 results
        "api_key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        # Find evoappliances.ca position
        position = None
        results = data.get('organic_results', [])
        
        for i, result in enumerate(results, 1):
            link = result.get('link', '')
            if TARGET_DOMAIN in link:
                position = i
                break
        
        return {
            'keyword': keyword,
            'position': position,
            'total_results': len(results),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'keyword': keyword,
            'position': None,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def load_previous_rankings():
    """Load previous day's rankings for comparison"""
    rankings_dir = '/root/.openclaw/workspace/rankings'
    
    # Find most recent file
    try:
        files = sorted([f for f in os.listdir(rankings_dir) if f.endswith('.json')])
        if files:
            with open(os.path.join(rankings_dir, files[-1])) as f:
                return json.load(f)
    except:
        pass
    
    return {}

def detect_changes(current, previous):
    """Detect significant ranking changes"""
    changes = []
    
    for curr in current:
        keyword = curr['keyword']
        curr_pos = curr.get('position')
        
        # Find previous position
        prev_pos = None
        for prev in previous.get('rankings', []):
            if prev['keyword'] == keyword:
                prev_pos = prev.get('position')
                break
        
        if prev_pos and curr_pos:
            change = prev_pos - curr_pos  # Positive = improved, Negative = dropped
            
            if change <= -3:  # Dropped 3+ positions
                changes.append({
                    'keyword': keyword,
                    'change': change,
                    'old_position': prev_pos,
                    'new_position': curr_pos,
                    'alert': 'DROPPED'
                })
            elif change >= 3:  # Improved 3+ positions
                changes.append({
                    'keyword': keyword,
                    'change': change,
                    'old_position': prev_pos,
                    'new_position': curr_pos,
                    'alert': 'IMPROVED'
                })
        elif prev_pos and not curr_pos:  # Was ranking, now not
            changes.append({
                'keyword': keyword,
                'change': 'LOST',
                'old_position': prev_pos,
                'new_position': None,
                'alert': 'LOST_RANKING'
            })
        elif not prev_pos and curr_pos:  # New ranking
            changes.append({
                'keyword': keyword,
                'change': 'NEW',
                'old_position': None,
                'new_position': curr_pos,
                'alert': 'NEW_RANKING'
            })
    
    return changes

def save_rankings(rankings):
    """Save rankings to file"""
    rankings_dir = '/root/.openclaw/workspace/rankings'
    os.makedirs(rankings_dir, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{rankings_dir}/{date_str}.json"
    
    data = {
        'date': date_str,
        'timestamp': datetime.now().isoformat(),
        'rankings': rankings
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filename

def generate_report(rankings, changes):
    """Generate ranking report"""
    report = []
    report.append("📊 EVO APPLIANCES RANKING REPORT")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # Summary
    total_keywords = len(rankings)
    ranked_keywords = sum(1 for r in rankings if r.get('position'))
    page1_keywords = sum(1 for r in rankings if r.get('position') and r['position'] <= 10)
    
    report.append(f"📈 SUMMARY:")
    report.append(f"   Total Keywords: {total_keywords}")
    report.append(f"   Ranking: {ranked_keywords}")
    report.append(f"   Page 1: {page1_keywords}")
    report.append("")
    
    # Rankings
    report.append("🎯 CURRENT RANKINGS:")
    for r in sorted(rankings, key=lambda x: x.get('position') or 999):
        pos = r.get('position')
        if pos:
            emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else "✅" if pos <= 10 else "⚠️"
            report.append(f"   {emoji} #{pos:2d} - {r['keyword']}")
        else:
            report.append(f"   ❌ Not ranking - {r['keyword']}")
    
    report.append("")
    
    # Changes
    if changes:
        report.append("🚨 CHANGES DETECTED:")
        for change in changes:
            if change['alert'] == 'DROPPED':
                report.append(f"   🔴 DROPPED: {change['keyword']}")
                report.append(f"      #{change['old_position']} → #{change['new_position']} ({change['change']} positions)")
            elif change['alert'] == 'IMPROVED':
                report.append(f"   🟢 IMPROVED: {change['keyword']}")
                report.append(f"      #{change['old_position']} → #{change['new_position']} (+{change['change']} positions)")
            elif change['alert'] == 'LOST_RANKING':
                report.append(f"   🔴 LOST: {change['keyword']}")
                report.append(f"      Was #{change['old_position']}, now not ranking")
            elif change['alert'] == 'NEW_RANKING':
                report.append(f"   🎉 NEW: {change['keyword']}")
                report.append(f"      Now ranking #{change['new_position']}")
    else:
        report.append("✅ No significant changes detected")
    
    return "\n".join(report)

def main():
    print("🔍 Starting rank tracking...")
    print(f"   Keywords: {len(KEYWORDS)}")
    print("")
    
    # Check all rankings
    rankings = []
    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"[{i}/{len(KEYWORDS)}] Checking: {keyword}")
        result = check_ranking(keyword)
        rankings.append(result)
        
        if result.get('position'):
            print(f"   ✅ Position: #{result['position']}")
        else:
            print(f"   ❌ Not ranking")
    
    # Load previous rankings
    previous = load_previous_rankings()
    
    # Detect changes
    changes = detect_changes(rankings, previous)
    
    # Save current rankings
    filename = save_rankings(rankings)
    print(f"\n💾 Rankings saved to: {filename}")
    
    # Generate report
    report = generate_report(rankings, changes)
    
    # Print report
    print("\n" + report)
    
    # Save report
    report_file = filename.replace('.json', '_report.txt')
    with open(report_file, 'w') as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    main()
