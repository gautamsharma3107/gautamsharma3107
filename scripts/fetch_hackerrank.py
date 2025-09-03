#!/usr/bin/env python3
"""
HackerRank Achievements Fetcher
Fetches achievements from HackerRank profile and generates README content
"""

import requests
import json
import re
from datetime import datetime
import os

class HackerRankFetcher:
    def __init__(self, username):
        self.username = username
        self.base_url = "https://www.hackerrank.com"
        self.profile_url = f"{self.base_url}/rest/hackers/{username}/recent_challenges"
        self.badges_url = f"{self.base_url}/rest/hackers/{username}/badges"
        
    def fetch_profile_data(self):
        """Fetch basic profile information"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Try to fetch profile page first
            profile_page_url = f"{self.base_url}/profile/{self.username}"
            response = requests.get(profile_page_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Extract data from the profile page
                content = response.text
                
                # Extract basic stats using regex patterns
                stats = self.extract_stats_from_html(content)
                return stats
            else:
                print(f"Failed to fetch profile: {response.status_code}")
                return self.get_fallback_data()
                
        except Exception as e:
            print(f"Error fetching profile data: {e}")
            return self.get_fallback_data()
    
    def extract_stats_from_html(self, html_content):
        """Extract statistics from HTML content"""
        stats = {
            'rank': 'N/A',
            'points': 'N/A',
            'badges': [],
            'solved_challenges': 'N/A',
            'certificates': []
        }
        
        try:
            # Extract rank
            rank_match = re.search(r'"rank":(\d+)', html_content)
            if rank_match:
                stats['rank'] = int(rank_match.group(1))
            
            # Extract points/score
            points_match = re.search(r'"score":([\d.]+)', html_content)
            if points_match:
                stats['points'] = float(points_match.group(1))
            
            # Extract solved challenges count
            solved_match = re.search(r'"solved":(\d+)', html_content)
            if solved_match:
                stats['solved_challenges'] = int(solved_match.group(1))
                
        except Exception as e:
            print(f"Error extracting stats: {e}")
            
        return stats
    
    def get_fallback_data(self):
        """Provide fallback data when API is not accessible"""
        return {
            'rank': 'N/A',
            'points': 'N/A', 
            'badges': ['Problem Solving', 'Python', 'C++', 'Algorithms', 'Data Structures'],
            'solved_challenges': 'N/A',
            'certificates': ['Problem Solving (Basic)', 'Python (Basic)'],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        }
    
    def generate_badges_markdown(self, stats):
        """Generate markdown for badges and achievements"""
        markdown = []
        
        # Header with HackerRank logo style
        markdown.append("🌟 **Actively solving challenges and improving problem-solving skills on HackerRank!**")
        markdown.append("")
        
        # Profile link with badge style
        profile_url = f"{self.base_url}/profile/{self.username}"
        markdown.append(f"[![HackerRank Profile](https://img.shields.io/badge/HackerRank-Profile-00EA64?style=for-the-badge&logo=hackerrank&logoColor=white)]({profile_url})")
        markdown.append("")
        
        # Statistics in a more visual format
        markdown.append("### 📊 Statistics")
        markdown.append("")
        
        # Create visual stats boxes
        stats_line = "| "
        
        if stats['rank'] != 'N/A':
            stats_line += f"🏆 **Rank**: #{stats['rank']:,} | "
        
        if stats['points'] != 'N/A':
            stats_line += f"⭐ **Points**: {stats['points']:,.1f} | "
            
        if stats['solved_challenges'] != 'N/A':
            stats_line += f"✅ **Solved**: {stats['solved_challenges']} | "
        
        # Remove trailing " | "
        stats_line = stats_line.rstrip(" | ")
        
        if len(stats_line) > 2:  # More than just "| "
            markdown.append(stats_line)
            markdown.append("")
        
        # Skills & Badges with improved styling
        if stats['badges']:
            markdown.append("### 🎯 Skills & Domains")
            markdown.append("")
            markdown.append("<div align=\"left\">")
            
            # Create badge images for each skill
            skill_badges = []
            for badge in stats['badges']:
                if badge.lower() == 'python':
                    skill_badges.append("![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)")
                elif badge.lower() == 'c++':
                    skill_badges.append("![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white)")
                elif 'problem solving' in badge.lower():
                    skill_badges.append("![Problem Solving](https://img.shields.io/badge/Problem_Solving-00EA64?style=flat-square&logo=hackerrank&logoColor=white)")
                elif badge.lower() == 'java':
                    skill_badges.append("![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=java&logoColor=white)")
                elif badge.lower() == 'javascript':
                    skill_badges.append("![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)")
                elif badge.lower() == 'algorithms':
                    skill_badges.append("![Algorithms](https://img.shields.io/badge/Algorithms-FF6B6B?style=flat-square&logo=codechef&logoColor=white)")
                elif 'data structures' in badge.lower():
                    skill_badges.append("![Data Structures](https://img.shields.io/badge/Data_Structures-4ECDC4?style=flat-square&logo=datacamp&logoColor=white)")
                else:
                    skill_badges.append(f"![{badge}](https://img.shields.io/badge/{badge.replace(' ', '_')}-00EA64?style=flat-square&logo=hackerrank&logoColor=white)")
            
            # Join badges with spaces
            markdown.append(" ".join(skill_badges))
            markdown.append("</div>")
            markdown.append("")
        
        # Add certificates section if available
        if stats.get('certificates'):
            markdown.append("### 🏆 Certifications")
            markdown.append("")
            for cert in stats['certificates']:
                markdown.append(f"- 🎖️ **{cert}**")
            markdown.append("")
        
        # Achievement highlights
        markdown.append("### 🚀 Recent Activity")
        markdown.append("")
        markdown.append("- 💪 **Active** on HackerRank solving algorithmic challenges")
        markdown.append("- 🎯 **Focus Areas**: Data Structures, Algorithms, Problem Solving")
        markdown.append("- 📈 **Growing** expertise in competitive programming")
        markdown.append("")
        
        # Call to action
        markdown.append(f"**[🔗 Visit my HackerRank Profile]({profile_url})**")
        markdown.append("")
        
        # Last updated
        updated_time = stats.get('last_updated', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'))
        markdown.append(f"<sub>Last updated: {updated_time}</sub>")
        
        return '\n'.join(markdown)
    
    def save_to_file(self, content, filename='hackerrank_stats.md'):
        """Save generated content to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully saved stats to {filename}")
        except Exception as e:
            print(f"Error saving to file: {e}")

def main():
    username = "gautamsharma3107"
    
    print(f"Fetching HackerRank achievements for {username}...")
    
    fetcher = HackerRankFetcher(username)
    stats = fetcher.fetch_profile_data()
    
    # Add timestamp
    stats['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    print(f"Fetched stats: {stats}")
    
    # Generate markdown content
    markdown_content = fetcher.generate_badges_markdown(stats)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), '..', 'hackerrank_stats.md')
    fetcher.save_to_file(markdown_content, output_file)
    
    print("HackerRank achievements updated successfully!")

if __name__ == "__main__":
    main()