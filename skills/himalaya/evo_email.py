#!/usr/bin/env python3
"""
Evo Appliances Email Automation
Backlink outreach and email management
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime

class EvoEmail:
    def __init__(self, smtp_host, smtp_port, imap_host, imap_port, email, password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.email = email
        self.password = password
        
    def send_backlink_outreach(self, to_email, site_name, contact_name=""):
        """Send personalized backlink outreach email"""
        
        subject = f"Quick question about {site_name}"
        
        body = f"""Hi {contact_name if contact_name else 'there'},

I hope this email finds you well. My name is [Name] from Evo Appliances, a local appliance repair company serving Vancouver and surrounding areas.

I came across {site_name} and really appreciated your [specific content about home maintenance/appliances]. Great resource for homeowners!

I noticed you have a resources/links section, and I was wondering if you'd be open to featuring a link to our appliance repair guide? We've put together a comprehensive guide that helps homeowners troubleshoot common appliance issues before calling a technician.

Here's the link: https://evoappliances.ca/appliance-repair-guide

We'd be happy to:
• Share your content with our social media followers (800+ local homeowners)
• Feature your site in our upcoming newsletter
• Write a guest post if you accept contributions

Would this be of interest? Either way, keep up the great work with {site_name}!

Best regards,
Evo Appliances Team
(604) 200-3054
https://evoappliances.ca
"""
        
        return self.send_email(to_email, subject, body)
    
    def send_email(self, to_email, subject, body):
        """Send a single email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            # Log sent email
            self._log_email('sent', to_email, subject)
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def check_inbox(self, limit=10):
        """Check recent emails"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(self.email, self.password)
            mail.select('inbox')
            
            _, data = mail.search(None, 'ALL')
            email_ids = data[0].split()[-limit:]
            
            emails = []
            for e_id in email_ids:
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append({
                    'from': msg['From'],
                    'subject': msg['Subject'],
                    'date': msg['Date']
                })
            
            mail.close()
            mail.logout()
            return emails
            
        except Exception as e:
            print(f"Error checking inbox: {e}")
            return []
    
    def _log_email(self, status, to_email, subject):
        """Log email activity"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'to': to_email,
            'subject': subject
        }
        
        log_file = '/root/.openclaw/.secrets/email_log.json'
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

# Usage examples:
if __name__ == "__main__":
    # Example: Send backlink outreach
    # evo = EvoEmail(
    #     smtp_host="smtp.gmail.com",
    #     smtp_port=465,
    #     imap_host="imap.gmail.com",
    #     imap_port=993,
    #     email="your@email.com",
    #     password="your-app-password"
    # )
    # evo.send_backlink_outreach("editor@site.com", "Vancouver Home Blog")
    pass
