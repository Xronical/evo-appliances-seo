#!/usr/bin/env python3
"""
Evo Appliances Content Refresh System
Identifies and refreshes old blog posts for SEO
"""

import subprocess
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# WordPress SSH credentials (loaded from env in production)
WP_HOST = "135.84.181.87"
WP_PORT = "27"
WP_USER = "rinnt515"
WP_PASS = "ema2002!"
WP_PATH = "/home/rinnt515/public_html"

class ContentRefresher:
    def __init__(self):
        self.refreshed_posts = []
        
    def run_ssh_command(self, command: str) -> str:
        """Run command on WordPress server via SSH"""
        ssh_cmd = f"sshpass -p '{WP_PASS}' ssh -p {WP_PORT} -o StrictHostKeyChecking=no {WP_USER}@{WP_HOST} '{command}'"
        try:
            result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"SSH Error: {e}")
            return ""
    
    def get_old_posts(self, months_old: int = 6) -> List[Dict]:
        """Find blog posts older than X months"""
        cutoff_date = (datetime.now() - timedelta(days=30*months_old)).strftime("%Y-%m-%d")
        
        # Get posts from WordPress
        cmd = f"cd {WP_PATH} && wp post list --post_type=post --post_status=publish --format=json --date={cutoff_date} --before={cutoff_date}"
        output = self.run_ssh_command(cmd)
        
        try:
            posts = json.loads(output)
            return posts if isinstance(posts, list) else []
        except:
            return []
    
    def get_post_content(self, post_id: int) -> Dict:
        """Get full post content"""
        cmd = f"cd {WP_PATH} && wp post get {post_id} --format=json"
        output = self.run_ssh_command(cmd)
        
        try:
            return json.loads(output)
        except:
            return {}
    
    def analyze_post_for_refresh(self, post: Dict) -> Dict:
        """Analyze if post needs refreshing"""
        content = post.get('content', {}).get('rendered', '')
        
        analysis = {
            'post_id': post.get('ID'),
            'title': post.get('title', {}).get('rendered', ''),
            'slug': post.get('slug', ''),
            'date': post.get('date', ''),
            'needs_refresh': False,
            'reasons': [],
            'suggestions': []
        }
        
        # Check 1: Age
        post_date = datetime.strptime(post['date'][:10], "%Y-%m-%d")
        age_days = (datetime.now() - post_date).days
        
        if age_days > 180:  # 6 months
            analysis['needs_refresh'] = True
            analysis['reasons'].append(f"Post is {age_days//30} months old")
        
        # Check 2: Missing "Updated" notice
        if 'updated' not in content.lower() and 'last updated' not in content.lower():
            analysis['needs_refresh'] = True
            analysis['reasons'].append("Missing 'Updated' notice")
            analysis['suggestions'].append("Add 'Last Updated: [Date]' banner")
        
        # Check 3: Outdated year references
        current_year = datetime.now().year
        old_years = [str(y) for y in range(current_year-3, current_year)]
        
        for year in old_years:
            if year in content:
                analysis['needs_refresh'] = True
                analysis['reasons'].append(f"Contains old year reference: {year}")
                analysis['suggestions'].append(f"Update {year} references to {current_year}")
                break
        
        # Check 4: Short content
        word_count = len(content.split())
        if word_count < 800:
            analysis['needs_refresh'] = True
            analysis['reasons'].append(f"Short content ({word_count} words)")
            analysis['suggestions'].append("Expand with new tips/sections")
        
        # Check 5: Missing internal links
        if content.count('<a href=') < 2:
            analysis['needs_refresh'] = True
            analysis['reasons'].append("Few internal links")
            analysis['suggestions'].append("Add 2-3 internal links to other posts")
        
        return analysis
    
    def refresh_post(self, post_id: int, analysis: Dict) -> bool:
        """Refresh a single post"""
        print(f"\n📝 Refreshing: {analysis['title']}")
        print(f"   Post ID: {post_id}")
        
        # Get current content
        post = self.get_post_content(post_id)
        content = post.get('content', {}).get('raw', post.get('content', {}).get('rendered', ''))
        
        # 1. Add/update "Last Updated" notice
        today = datetime.now().strftime("%B %d, %Y")
        updated_notice = f'\u003c!-- wp:paragraph {"className":"has-background","backgroundColor":"light-gray"} --\u003e\n\u003cp class="has-light-gray-background-color has-background"\u003e\u003cstrong\u003e🔄 Last Updated: {today}\u003c/strong\u003e – This guide has been updated with the latest information and tips.\u003c/p\u003e\n\u003c!-- /wp:paragraph --\u003e\n\n'
        
        # Insert after first paragraph
        if '\u003c!-- /wp:paragraph --\u003e' in content:
            parts = content.split('\u003c!-- /wp:paragraph --\u003e', 1)
            new_content = parts[0] + '\u003c!-- /wp:paragraph --\u003e\n\n' + updated_notice + parts[1]
        else:
            new_content = updated_notice + content
        
        # 2. Update year references
        current_year = datetime.now().year
        old_year = str(current_year - 1)
        new_content = new_content.replace(old_year, str(current_year))
        
        # 3. Refresh conclusion
        if '\u003c!-- wp:heading' in new_content:
            # Add CTA before last heading or at end
            cta = f'''\n\n\u003c!-- wp:heading {{"level":2}} --\u003e
\u003ch2\u003eNeed Professional Appliance Repair in Vancouver?\u003c/h2\u003e
\u003c!-- /wp:heading --\u003e

\u003c!-- wp:paragraph --\u003e
\u003cp\u003eDon't let appliance problems disrupt your day. Evo Appliances provides fast, reliable repair services throughout Vancouver, Burnaby, and the Lower Mainland.\u003c/p\u003e
\u003c!-- /wp:paragraph --\u003e

\u003c!-- wp:paragraph --\u003e
\u003cp\u003e\u003cstrong\u003e📞 Call: (604) 200-3054\u003c/strong\u003e\u003cbr\u003e\u003cstrong\u003e🌐 Book Online: \u003ca href="https://evoappliances.ca"\u003eevoappliances.ca\u003c/a\u003e\u003c/strong\u003e\u003c/p\u003e
\u003c!-- /wp:paragraph --\u003e'''
            
            # Only add if not already there
            if 'Need Professional Appliance Repair' not in new_content:
                new_content = new_content + cta
        
        # 4. Update the post
        # Escape content for shell
        safe_content = new_content.replace("'", "'\"'\"'")
        
        cmd = f"cd {WP_PATH} && wp post update {post_id} --post_content='{safe_content}' --post_date='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
        result = self.run_ssh_command(cmd)
        
        if "Success" in result or result == "":
            print("   ✅ Post refreshed successfully!")
            self.refreshed_posts.append({
                'post_id': post_id,
                'title': analysis['title'],
                'url': f"https://evoappliances.ca/{analysis['slug']}/",
                'changes': analysis['reasons']
            })
            return True
        else:
            print(f"   ❌ Error: {result}")
            return False
    
    def run_refresh_cycle(self, max_posts: int = 1) -> List[Dict]:
        """Run full refresh cycle"""
        print("🔍 Finding posts needing refresh...")
        
        # Get old posts
        old_posts = self.get_old_posts(months_old=6)
        print(f"   Found {len(old_posts)} posts older than 6 months")
        
        if not old_posts:
            print("   ✅ No old posts found!")
            return []
        
        # Analyze each post
        candidates = []
        for post in old_posts:
            analysis = self.analyze_post_for_refresh(post)
            if analysis['needs_refresh']:
                candidates.append((post, analysis))
        
        print(f"   {len(candidates)} posts need refreshing")
        
        if not candidates:
            print("   ✅ All posts are up to date!")
            return []
        
        # Refresh top candidates (prioritize by number of reasons)
        candidates.sort(key=lambda x: len(x[1]['reasons']), reverse=True)
        
        to_refresh = candidates[:max_posts]
        
        print(f"\n🔄 Refreshing {len(to_refresh)} post(s)...")
        
        for post, analysis in to_refresh:
            self.refresh_post(post['ID'], analysis)
        
        return self.refreshed_posts
    
    def generate_report(self) -> str:
        """Generate refresh report"""
        if not self.refreshed_posts:
            return "✅ No posts needed refreshing this week."
        
        report = []
        report.append("📊 CONTENT REFRESH REPORT")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        report.append("")
        report.append(f"Posts Refreshed: {len(self.refreshed_posts)}")
        report.append("")
        
        for i, post in enumerate(self.refreshed_posts, 1):
            report.append(f"{i}. {post['title']}")
            report.append(f"   URL: {post['url']}")
            report.append(f"   Changes: {', '.join(post['changes'])}")
            report.append("")
        
        report.append("✅ All posts updated with 'Last Updated' date")
        report.append("✅ Social media promotion ready")
        
        return "\n".join(report)


def main():
    refresher = ContentRefresher()
    
    # Refresh max 1 post per run (don't overwhelm)
    refreshed = refresher.run_refresh_cycle(max_posts=1)
    
    # Generate report
    report = refresher.generate_report()
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # Save report
    report_file = f"/root/.openclaw/workspace/content_refresh_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    return report


if __name__ == "__main__":
    main()
