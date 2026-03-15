#!/usr/bin/env python3
"""
Google Search Console Data Puller for Evo Appliances
Pulls search performance data daily
"""

import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SERVICE_ACCOUNT_FILE = '/root/.openclaw/.secrets/google-cloud.env'
SITE_URL = 'https://evoappliances.ca/'
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

# Service account credentials
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "evo-appliance-repair-395115",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqIFSJOR5l+mJT
bVrI2oVf+C9a3LdAxCKgPw8jpUaVHa4i/gI8UZxSIZRbmPRBKHBx5u8mhDf+f4UT
Tsefh/GHE7lBqnAyCWAhJ0FdDUXWbxGuMAtJe3ZP/45x7R6aOYLPCHyH9dwCtdQT
piJ/P8nySfDASR61lLDMaBadRpljWy4FkRnzgznUUIuTsPvXwV6lQodoUrNBjyup
QYdx2p8PXMI2Arw/uagMuRTPQoKJ1po3X07G81ZBKSUt/+vItxsJQlUAdeP5Py7v
FPta0fgSslFBVoKnSZWIWLlH9p2znTEUVL3TZCVh2N4xP6zRndmIu9EGUYf21Kip
SMWNhRxNAgMBAAECggEABBFMfKpdv7JxIP6U4VzHGfzYT6xf0ydDwgImXbcDxuAj
Dw7bJ1xykF2/TUJq8n15TGICug5cCF8KjmywksU5DNxmh+x3CKoqUjo0cqyS1Up7
E98YmTCkGe4Wjg+RkzXgAS7xsbChTtFqH5rxz6xCgFqkORbbzJMX75gAtq6+xsjL
L21S7mUkkf42MBMJcY21Z1y77y99HHS4H5jghU5ZqgPoQH4EEP7baVuDKxAZz4mj
Xa0LANtkTB+JCQUYGLG9XY6oHRqpITDOzfArUQtX4a2kGtzkb4OPXrtJLuBd+ChG
02lIfiqYtcmNvJsYRBow7DgMYA1XPM1f4SckJ4ndQQKBgQDb9dtR7zrV6QAYLw4p
6fVhR+wxE7MlmtcBJ8+htB4K3sdsnJrwmIBAhFki2QKxG2ICIrlHMeDEpPjJyhsl
NsE+TpNDt19Tzo4V47i0jRfw6h3mV6CENbKQtDDXpbnIgV0v8wz6LmsrwJjn9oEQ
3RdVgIM5S9Uz8ls7bJ2h4wGfrwKBgQDGADRDZqUjqxPc7l6FMq8k92O9d4cQUWCh
3wmqcDKNa7Vguw+Rb1ROUN80rZFzYr0jWIvdlAcYqPs72BZvGa0/etrA8YAyZCUp
SCxoww3Jbm4t7IKzDMbGw22D9bhhqG3ULRzdyZZC7yBdyLl04EHniaF+AeqrPLTf
GbalMFOmwwKBgQCaUJ/vmaBzViXk0Y5kRWkLOMQxohp69WiFvQJj9dNl2Omb/zqM
NNE1ciR+2DSVQBrAWNAXbJy+GOcZ2pq0vvdP2Rxj05AjYbQ5EywQLzRupjEX2r4Y
QvvlnSTvBauTSX6xFxkxo8M4TMR5aG0gAZxPNfvaBKOs8AilZgwo+PO4rQKBgQC1
NkKe3TaOamiHbvG63iRFpNT39oj6ekACZeqmvoDFxan+mbUp2cZC1ukxgRj5jYik
7Mk1ReEoxJ8Kqj39+HYC/yFuLJizhcws+A0M5Fed3x+fkDIeRLc3+mwktaLGXiwG
YDNnGLQZFll8+9QgD47BpcjTVlW72pd/CD2M+anVmQKBgG6Ku4Eb2HM5L2HBbIt0
73hXamiajVXFD0rIfH3+oGHhJWUJoxcGGjtpV/VH/k377vudzJWUj4axhynnopoO
EFKdyXm5c18OHr4PhnEyM1dLgtaqlEbMGG9CK2WowfXje1rR7mljo5LlH+726h3S
6Qtf7DmjnD7ps0wnVVdUOUhw
-----END PRIVATE KEY-----""",
    "client_email": "evo-analytics-api@evo-appliance-repair-395115.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}

def get_search_console_service():
    """Get Search Console API service"""
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO,
        scopes=SCOPES
    )
    return build('webmasters', 'v3', credentials=credentials)

def get_query_data(service, days=7, limit=50):
    """Get top search queries"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    request_body = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['query'],
        'rowLimit': limit
    }
    
    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request_body
    ).execute()
    
    queries = []
    if 'rows' in response:
        for row in response['rows']:
            queries.append({
                'query': row['keys'][0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': round(row.get('ctr', 0) * 100, 2),
                'position': round(row.get('position', 0), 1)
            })
    
    return queries

def get_page_data(service, days=7, limit=50):
    """Get top pages"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    request_body = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['page'],
        'rowLimit': limit
    }
    
    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request_body
    ).execute()
    
    pages = []
    if 'rows' in response:
        for row in response['rows']:
            pages.append({
                'page': row['keys'][0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': round(row.get('ctr', 0) * 100, 2),
                'position': round(row.get('position', 0), 1)
            })
    
    return pages

def get_date_comparison(service, days=7):
    """Compare current period vs previous period"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    prev_end = start_date - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days)
    
    # Current period
    current = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body={
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'dimensions': [],
            'rowLimit': 1
        }
    ).execute()
    
    # Previous period
    previous = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body={
            'startDate': prev_start.strftime('%Y-%m-%d'),
            'endDate': prev_end.strftime('%Y-%m-%d'),
            'dimensions': [],
            'rowLimit': 1
        }
    ).execute()
    
    current_data = current['rows'][0] if 'rows' in current else {}
    previous_data = previous['rows'][0] if 'rows' in previous else {}
    
    return {
        'current': {
            'clicks': current_data.get('clicks', 0),
            'impressions': current_data.get('impressions', 0),
            'ctr': round(current_data.get('ctr', 0) * 100, 2)
        },
        'previous': {
            'clicks': previous_data.get('clicks', 0),
            'impressions': previous_data.get('impressions', 0),
            'ctr': round(previous_data.get('ctr', 0) * 100, 2)
        }
    }

def generate_report(data):
    """Generate markdown report"""
    report = []
    report.append("# Google Search Console Report - Evo Appliances")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append(f"Period: Last {data['period_days']} days")
    report.append("")
    
    # Summary
    report.append("## Summary")
    report.append("")
    comparison = data['comparison']
    report.append(f"**Current Period:**")
    report.append(f"- Clicks: {comparison['current']['clicks']}")
    report.append(f"- Impressions: {comparison['current']['impressions']}")
    report.append(f"- CTR: {comparison['current']['ctr']}%")
    report.append("")
    report.append(f"**Previous Period:**")
    report.append(f"- Clicks: {comparison['previous']['clicks']}")
    report.append(f"- Impressions: {comparison['previous']['impressions']}")
    report.append(f"- CTR: {comparison['previous']['ctr']}%")
    report.append("")
    
    # Top Queries
    report.append("## Top Search Queries")
    report.append("")
    report.append("| Query | Clicks | Impressions | CTR | Position |")
    report.append("|-------|--------|-------------|-----|----------|")
    
    for q in data['top_queries'][:20]:
        report.append(f"| {q['query'][:40]} | {q['clicks']} | {q['impressions']} | {q['ctr']}% | {q['position']} |")
    
    report.append("")
    
    # Top Pages
    report.append("## Top Pages")
    report.append("")
    report.append("| Page | Clicks | Impressions | CTR | Position |")
    report.append("|------|--------|-------------|-----|----------|")
    
    for p in data['top_pages'][:10]:
        page_short = p['page'].replace('https://evoappliances.ca/', '/')
        report.append(f"| {page_short[:40]} | {p['clicks']} | {p['impressions']} | {p['ctr']}% | {p['position']} |")
    
    report.append("")
    
    # Opportunities
    report.append("## Opportunities")
    report.append("")
    report.append("Queries with high impressions but low clicks (optimize these):")
    report.append("")
    
    opportunities = [q for q in data['top_queries'] if q['impressions'] > 20 and q['clicks'] < 2]
    for q in opportunities[:10]:
        report.append(f"- **{q['query']}**: {q['impressions']} impressions, {q['clicks']} clicks ({q['ctr']}% CTR)")
    
    return "\n".join(report)

def main():
    print("="*60)
    print("Google Search Console Data Pull")
    print("="*60)
    print()
    
    try:
        service = get_search_console_service()
        print("✅ Connected to Search Console API")
        print()
        
        # Get data
        print("📊 Fetching query data...")
        queries = get_query_data(service, days=7, limit=50)
        print(f"   Found {len(queries)} queries")
        
        print("📄 Fetching page data...")
        pages = get_page_data(service, days=7, limit=50)
        print(f"   Found {len(pages)} pages")
        
        print("📈 Fetching comparison data...")
        comparison = get_date_comparison(service, days=7)
        print("   Done")
        
        # Compile data
        data = {
            'scraped_at': datetime.now().isoformat(),
            'period_days': 7,
            'site': SITE_URL,
            'top_queries': queries,
            'top_pages': pages,
            'comparison': comparison
        }
        
        # Save JSON
        data_dir = '/root/.openclaw/workspace/data'
        os.makedirs(data_dir, exist_ok=True)
        
        json_file = f'{data_dir}/search-console-data.json'
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Generate report
        report = generate_report(data)
        report_file = f'{data_dir}/search-console-report.md'
        with open(report_file, 'w') as f:
            f.write(report)
        
        print()
        print("="*60)
        print("✅ Data saved successfully!")
        print("="*60)
        print()
        print(f"📁 JSON: {json_file}")
        print(f"📄 Report: {report_file}")
        print()
        print("📊 Summary:")
        print(f"   Clicks (7 days): {comparison['current']['clicks']}")
        print(f"   Impressions (7 days): {comparison['current']['impressions']}")
        print(f"   CTR: {comparison['current']['ctr']}%")
        print()
        print("🔍 Top 5 Queries:")
        for i, q in enumerate(queries[:5], 1):
            print(f"   {i}. {q['query'][:45]} ({q['clicks']} clicks)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
