#!/usr/bin/env python3
"""
Google Analytics 4 Data Puller for Evo Appliances
Pulls traffic and conversion data daily
"""

import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
GA4_PROPERTY_ID = "309639007"
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

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

def get_ga4_service():
    """Get GA4 Analytics Data API service"""
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO,
        scopes=SCOPES
    )
    return build('analyticsdata', 'v1beta', credentials=credentials)

def get_traffic_overview(service, days=7):
    """Get traffic overview"""
    property_name = f"properties/{GA4_PROPERTY_ID}"
    
    request_body = {
        'dateRanges': [{'startDate': f'{days}daysAgo', 'endDate': 'today'}],
        'metrics': [
            {'name': 'sessions'},
            {'name': 'totalUsers'},
            {'name': 'newUsers'},
            {'name': 'bounceRate'},
            {'name': 'averageSessionDuration'},
            {'name': 'conversions'}
        ]
    }
    
    response = service.properties().runReport(
        property=property_name,
        body=request_body
    ).execute()
    
    if 'rows' in response and len(response['rows']) > 0:
        row = response['rows'][0]
        metrics = row['metricValues']
        return {
            'sessions': int(metrics[0]['value']),
            'totalUsers': int(metrics[1]['value']),
            'newUsers': int(metrics[2]['value']),
            'bounceRate': round(float(metrics[3]['value']) * 100, 2),
            'avgSessionDuration': round(float(metrics[4]['value']), 2),
            'conversions': int(metrics[5]['value'])
        }
    return {}

def get_traffic_sources(service, days=7):
    """Get traffic by source"""
    property_name = f"properties/{GA4_PROPERTY_ID}"
    
    request_body = {
        'dateRanges': [{'startDate': f'{days}daysAgo', 'endDate': 'today'}],
        'dimensions': [{'name': 'sessionDefaultChannelGroup'}],
        'metrics': [
            {'name': 'sessions'},
            {'name': 'totalUsers'}
        ],
        'orderBys': [{'metric': {'metricName': 'sessions'}, 'desc': True}]
    }
    
    response = service.properties().runReport(
        property=property_name,
        body=request_body
    ).execute()
    
    sources = []
    if 'rows' in response:
        for row in response['rows']:
            sources.append({
                'channel': row['dimensionValues'][0]['value'],
                'sessions': int(row['metricValues'][0]['value']),
                'users': int(row['metricValues'][1]['value'])
            })
    return sources

def get_top_pages(service, days=7, limit=10):
    """Get top pages"""
    property_name = f"properties/{GA4_PROPERTY_ID}"
    
    request_body = {
        'dateRanges': [{'startDate': f'{days}daysAgo', 'endDate': 'today'}],
        'dimensions': [{'name': 'pageTitle'}, {'name': 'pagePath'}],
        'metrics': [
            {'name': 'sessions'},
            {'name': 'totalUsers'}
        ],
        'orderBys': [{'metric': {'metricName': 'sessions'}, 'desc': True}],
        'limit': limit
    }
    
    response = service.properties().runReport(
        property=property_name,
        body=request_body
    ).execute()
    
    pages = []
    if 'rows' in response:
        for row in response['rows']:
            pages.append({
                'title': row['dimensionValues'][0]['value'],
                'path': row['dimensionValues'][1]['value'],
                'sessions': int(row['metricValues'][0]['value']),
                'users': int(row['metricValues'][1]['value'])
            })
    return pages

def get_device_breakdown(service, days=7):
    """Get device breakdown"""
    property_name = f"properties/{GA4_PROPERTY_ID}"
    
    request_body = {
        'dateRanges': [{'startDate': f'{days}daysAgo', 'endDate': 'today'}],
        'dimensions': [{'name': 'deviceCategory'}],
        'metrics': [{'name': 'sessions'}]
    }
    
    response = service.properties().runReport(
        property=property_name,
        body=request_body
    ).execute()
    
    devices = []
    if 'rows' in response:
        for row in response['rows']:
            devices.append({
                'device': row['dimensionValues'][0]['value'],
                'sessions': int(row['metricValues'][0]['value'])
            })
    return devices

def generate_report(data):
    """Generate markdown report"""
    report = []
    report.append("# Google Analytics 4 Report - Evo Appliances")
    report.append(f"Generated: {data['generated_at']}")
    report.append(f"Period: Last {data['period_days']} days")
    report.append("")
    
    # Overview
    overview = data['overview']
    report.append("## Traffic Overview")
    report.append("")
    report.append(f"- **Sessions:** {overview.get('sessions', 0)}")
    report.append(f"- **Total Users:** {overview.get('totalUsers', 0)}")
    report.append(f"- **New Users:** {overview.get('newUsers', 0)}")
    report.append(f"- **Bounce Rate:** {overview.get('bounceRate', 0)}%")
    report.append(f"- **Avg Session Duration:** {overview.get('avgSessionDuration', 0)}s")
    report.append(f"- **Conversions:** {overview.get('conversions', 0)}")
    report.append("")
    
    # Traffic Sources
    report.append("## Traffic Sources")
    report.append("")
    report.append("| Channel | Sessions | Users |")
    report.append("|---------|----------|-------|")
    for source in data['sources']:
        report.append(f"| {source['channel']} | {source['sessions']} | {source['users']} |")
    report.append("")
    
    # Top Pages
    report.append("## Top Pages")
    report.append("")
    report.append("| Page | Sessions | Users |")
    report.append("|------|----------|-------|")
    for page in data['top_pages']:
        path = page['path'][:40] if len(page['path']) > 40 else page['path']
        report.append(f"| {path} | {page['sessions']} | {page['users']} |")
    report.append("")
    
    # Device Breakdown
    report.append("## Device Breakdown")
    report.append("")
    report.append("| Device | Sessions |")
    report.append("|--------|----------|")
    for device in data['devices']:
        report.append(f"| {device['device'].title()} | {device['sessions']} |")
    report.append("")
    
    # Insights
    report.append("## Insights")
    report.append("")
    
    total_sessions = overview.get('sessions', 0)
    if total_sessions > 0:
        organic = next((s['sessions'] for s in data['sources'] if s['channel'] == 'Organic Search'), 0)
        organic_pct = round(organic / total_sessions * 100, 1)
        report.append(f"- **Organic Search:** {organic_pct}% of traffic ({organic} sessions)")
        
        direct = next((s['sessions'] for s in data['sources'] if s['channel'] == 'Direct'), 0)
        direct_pct = round(direct / total_sessions * 100, 1)
        report.append(f"- **Direct Traffic:** {direct_pct}% of traffic ({direct} sessions)")
    
    report.append(f"- **New vs Returning:** {overview.get('newUsers', 0)} new, {overview.get('users', 0) - overview.get('newUsers', 0)} returning")
    
    return "\n".join(report)

def main():
    print("="*60)
    print("Google Analytics 4 Data Pull")
    print("="*60)
    print()
    
    try:
        service = get_ga4_service()
        print("✅ Connected to GA4 API")
        print()
        
        # Get data
        print("📊 Fetching traffic overview...")
        overview = get_traffic_overview(service, days=7)
        print(f"   Sessions: {overview.get('sessions', 0)}")
        
        print("📈 Fetching traffic sources...")
        sources = get_traffic_sources(service, days=7)
        print(f"   Found {len(sources)} channels")
        
        print("📄 Fetching top pages...")
        pages = get_top_pages(service, days=7)
        print(f"   Found {len(pages)} pages")
        
        print("📱 Fetching device breakdown...")
        devices = get_device_breakdown(service, days=7)
        print(f"   Found {len(devices)} device types")
        
        # Compile data
        data = {
            'generated_at': datetime.now().isoformat(),
            'period_days': 7,
            'property_id': GA4_PROPERTY_ID,
            'overview': overview,
            'sources': sources,
            'top_pages': pages,
            'devices': devices
        }
        
        # Save JSON
        data_dir = '/root/.openclaw/workspace/data'
        os.makedirs(data_dir, exist_ok=True)
        
        json_file = f'{data_dir}/ga4-data.json'
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Generate report
        report = generate_report(data)
        report_file = f'{data_dir}/ga4-report.md'
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
        print(f"   Sessions: {overview.get('sessions', 0)}")
        print(f"   Total Users: {overview.get('totalUsers', 0)}")
        print(f"   Bounce Rate: {overview.get('bounceRate', 0)}%")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
