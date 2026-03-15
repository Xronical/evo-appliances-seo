#!/usr/bin/env python3
"""
Test Google API Access for Evo Appliances
Checks GA4 and Search Console access
"""

import os
import json
from datetime import datetime, timedelta

# Load service account credentials
import sys
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    print("✅ Google API libraries available")
except ImportError:
    print("❌ Google API libraries not installed")
    print("Installing...")
    os.system("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client --break-system-packages -q")
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

# Configuration
GA4_PROPERTY_ID = "309639007"
SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/webmasters.readonly'
]

# Service account info
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "evo-appliance-repair-395115",
    "private_key_id": "evo-analytics-api",
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
    "client_id": "104661493823456789",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
}

def test_ga4_access():
    """Test GA4 API access"""
    print("\n" + "="*60)
    print("Testing GA4 Access")
    print("="*60)
    
    try:
        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )
        
        # Build the Analytics Data API service
        analytics = build('analyticsdata', 'v1beta', credentials=credentials)
        
        # Try to get property metadata
        property_name = f"properties/{GA4_PROPERTY_ID}"
        
        # Try a simple query
        request_body = {
            'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
            'metrics': [{'name': 'sessions'}]
        }
        
        response = analytics.properties().runReport(
            property=property_name,
            body=request_body
        ).execute()
        
        print("✅ GA4 Access: SUCCESS")
        print(f"   Property: {GA4_PROPERTY_ID}")
        if 'rows' in response:
            print(f"   Sessions (last 7 days): {response['rows'][0]['metricValues'][0]['value']}")
        return True
        
    except Exception as e:
        print("❌ GA4 Access: FAILED")
        print(f"   Error: {str(e)[:200]}")
        return False

def test_search_console_access():
    """Test Search Console API access"""
    print("\n" + "="*60)
    print("Testing Search Console Access")
    print("="*60)
    
    try:
        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO,
            scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )
        
        # Build Search Console API service
        webmasters = build('webmasters', 'v3', credentials=credentials)
        
        # Try to list sites
        sites = webmasters.sites().list().execute()
        
        print("✅ Search Console Access: SUCCESS")
        
        if 'siteEntry' in sites:
            print(f"   Sites found: {len(sites['siteEntry'])}")
            for site in sites['siteEntry'][:5]:
                site_url = site.get('siteUrl', 'Unknown')
                permission = site.get('permissionLevel', 'Unknown')
                print(f"   - {site_url} ({permission})")
                
                # If evoappliances.ca is found, test query data
                if 'evoappliances' in site_url:
                    print(f"\n   📊 Testing query data for {site_url}...")
                    try:
                        request_body = {
                            'startDate': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                            'endDate': datetime.now().strftime('%Y-%m-%d'),
                            'dimensions': ['query'],
                            'rowLimit': 10
                        }
                        
                        response = webmasters.searchanalytics().query(
                            siteUrl=site_url,
                            body=request_body
                        ).execute()
                        
                        if 'rows' in response:
                            print(f"   ✅ Query data retrieved: {len(response['rows'])} queries")
                            for row in response['rows'][:3]:
                                query = row['keys'][0]
                                clicks = row.get('clicks', 0)
                                impressions = row.get('impressions', 0)
                                print(f"      - {query}: {clicks} clicks, {impressions} impressions")
                    except Exception as e2:
                        print(f"   ⚠️ Could not retrieve query data: {str(e2)[:100]}")
        else:
            print("   No sites found")
            print("   The service account may not have access to any Search Console properties")
        
        return True
        
    except Exception as e:
        print("❌ Search Console Access: FAILED")
        print(f"   Error: {str(e)[:200]}")
        return False

def main():
    print("="*60)
    print("Google API Access Test for Evo Appliances")
    print("="*60)
    print(f"Service Account: {SERVICE_ACCOUNT_INFO['client_email']}")
    print(f"GA4 Property: {GA4_PROPERTY_ID}")
    print(f"Domain: evoappliances.ca")
    
    # Test GA4
    ga4_ok = test_ga4_access()
    
    # Test Search Console
    gsc_ok = test_search_console_access()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"GA4 Access: {'✅ WORKING' if ga4_ok else '❌ NOT WORKING'}")
    print(f"Search Console Access: {'✅ WORKING' if gsc_ok else '❌ NOT WORKING'}")
    
    if not ga4_ok or not gsc_ok:
        print("\n🔧 TO FIX:")
        if not ga4_ok:
            print("1. Go to GA4 Admin → Property Access Management")
            print("2. Add: evo-analytics-api@evo-appliance-repair-395115.iam.gserviceaccount.com")
            print("3. Grant 'Viewer' or 'Analyst' role")
        if not gsc_ok:
            print("1. Go to Search Console → Settings → Users and Permissions")
            print("2. Add: evo-analytics-api@evo-appliance-repair-395115.iam.gserviceaccount.com")
            print("3. Grant 'Full' or 'Restricted' permission")

if __name__ == "__main__":
    main()
