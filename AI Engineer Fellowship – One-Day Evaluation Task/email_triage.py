#!/usr/bin/env python3
"""
Smart Email Triage System
AI-driven workflow for automatic email classification and alerting
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Tuple
import re
from collections import Counter

class EmailTriageSystem:
    def __init__(self):
        self.categories = ["Product Support", "Billing", "General Inquiry"]
        self.processed_emails = []
        
    def classify_and_summarize_email(self, email_content: str, sender: str) -> Tuple[str, str]:
        """
        Simulate AI classification and summarization
        In production, this would call OpenAI/Claude API
        """
        email_lower = email_content.lower()
        
        # Simple rule-based classification (simulating AI)
        if any(word in email_lower for word in ['bug', 'error', 'not working', 'broken', 'crash', 'issue', 'problem', 'feature', 'how to']):
            category = "Product Support"
        elif any(word in email_lower for word in ['bill', 'payment', 'charge', 'invoice', 'refund', 'subscription', 'pricing', 'cost']):
            category = "Billing"
        else:
            category = "General Inquiry"
        
        # Generate summary (simulating AI summarization)
        first_sentence = email_content.split('.')[0][:100]
        summary = f"Customer {sender} needs help with {category.lower()}: {first_sentence}..."
        
        return category, summary
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common words and extract keywords
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their'}
        
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        return keywords
    
    def process_email(self, email_data: Dict) -> Dict:
        """Process a single email through the triage system"""
        sender = email_data['sender']
        subject = email_data['subject']
        content = email_data['content']
        
        # Combine subject and content for analysis
        full_content = f"{subject} {content}"
        
        # Classify and summarize
        category, summary = self.classify_and_summarize_email(full_content, sender)
        
        # Extract keywords
        keywords = self.extract_keywords(full_content)
        
        # Create processed email record
        processed_email = {
            'timestamp': datetime.now().isoformat(),
            'sender': sender,
            'subject': subject,
            'category': category,
            'summary': summary,
            'keywords': keywords,
            'channel': f"#{category.lower().replace(' ', '-')}"
        }
        
        self.processed_emails.append(processed_email)
        return processed_email
    
    def send_slack_alert(self, processed_email: Dict):
        """Simulate sending Slack alert (in production, use Slack API)"""
        channel = processed_email['channel']
        summary = processed_email['summary']
        sender = processed_email['sender']
        
        alert_message = f"🚨 New {processed_email['category']} Email\n" \
                       f"From: {sender}\n" \
                       f"Summary: {summary}\n" \
                       f"Channel: {channel}"
        
        print(f"\n📤 SLACK ALERT SENT TO {channel}:")
        print(f"   {summary}")
        print(f"   From: {sender}")
        return alert_message
    
    def generate_keyword_analytics(self) -> Dict[str, List[str]]:
        """Generate top 5 keywords per category"""
        analytics = {}
        
        for category in self.categories:
            category_emails = [email for email in self.processed_emails if email['category'] == category]
            all_keywords = []
            
            for email in category_emails:
                all_keywords.extend(email['keywords'])
            
            # Get top 5 keywords
            keyword_counts = Counter(all_keywords)
            top_keywords = [word for word, count in keyword_counts.most_common(5)]
            analytics[category] = top_keywords
        
        return analytics
    
    def save_to_csv(self, filename: str = 'email_triage_log.csv'):
        """Save triage results to CSV file"""
        if not self.processed_emails:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'sender', 'subject', 'category', 'summary', 'keywords', 'channel']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for email in self.processed_emails:
                # Convert keywords list to string for CSV
                email_copy = email.copy()
                email_copy['keywords'] = ', '.join(email['keywords'])
                writer.writerow(email_copy)
        
        print(f"\n💾 Results saved to {filename}")
    
    def save_to_json(self, filename: str = 'email_triage_log.json'):
        """Save triage results to JSON file"""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.processed_emails, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to {filename}")

def main():
    """Main workflow execution"""
    print("🤖 Smart Email Triage System Starting...")
    print("=" * 50)
    
    # Initialize the system
    triage_system = EmailTriageSystem()
    
    # Sample emails (simulating incoming emails)
    sample_emails = [
        {
            "sender": "john.doe@example.com",
            "subject": "Login not working",
            "content": "I can't log into my account. Getting error message 'Invalid credentials' but I'm sure my password is correct. This is very urgent as I need to access my dashboard for a client meeting."
        },
        {
            "sender": "sarah.smith@company.com",
            "subject": "Billing Question",
            "content": "Hi, I was charged $99 last month but I thought my subscription was only $49. Can you please check my billing details and explain this charge?"
        },
        {
            "sender": "mike.wilson@startup.io",
            "subject": "Partnership Inquiry",
            "content": "Hello, we're interested in exploring a potential partnership opportunity. We're a fintech startup looking to integrate your API services. Could we schedule a call to discuss this further?"
        },
        {
            "sender": "lisa.brown@tech.com",
            "subject": "Feature Request - Dark Mode",
            "content": "Love your product! Would it be possible to add a dark mode feature? Many users including myself would really appreciate this addition to reduce eye strain during late-night work sessions."
        },
        {
            "sender": "david.lee@business.org",
            "subject": "Refund Request",
            "content": "I need to cancel my subscription and get a refund for this month. I haven't used the service as expected and would like to process this cancellation immediately."
        }
    ]
    
    # Process each email
    for i, email in enumerate(sample_emails, 1):
        print(f"\n Processing Email {i}/{len(sample_emails)}...")
        processed_email = triage_system.process_email(email)
        triage_system.send_slack_alert(processed_email)
    
    # Generate analytics
    print(f"\n KEYWORD ANALYTICS:")
    print("=" * 30)
    analytics = triage_system.generate_keyword_analytics()
    for category, keywords in analytics.items():
        print(f"{category}: {', '.join(keywords) if keywords else 'No keywords'}")
    
    # Save results
    print(f"\n SAVING RESULTS:")
    print("=" * 20)
    triage_system.save_to_csv()
    triage_system.save_to_json()
    
    # Summary
    total_emails = len(triage_system.processed_emails)
    category_counts = {}
    for email in triage_system.processed_emails:
        category = email['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print(f"\n SUMMARY:")
    print("=" * 15)
    print(f"Total emails processed: {total_emails}")
    for category, count in category_counts.items():
        print(f"{category}: {count} emails")
    
    print(f"\n Email triage workflow completed successfully!")

if __name__ == "__main__":

    main()
