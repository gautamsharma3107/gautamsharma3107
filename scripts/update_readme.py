#!/usr/bin/env python3
"""
README updater for HackerRank achievements
Updates the README.md file with the latest HackerRank stats
"""

import os
import re

def update_readme():
    """Update README.md with HackerRank achievements"""
    
    # Paths
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    stats_path = os.path.join(os.path.dirname(__file__), '..', 'hackerrank_stats.md')
    output_path = os.path.join(os.path.dirname(__file__), '..', 'README_updated.md')
    
    # Check if stats file exists
    if not os.path.exists(stats_path):
        print("HackerRank stats file not found")
        return False
    
    # Read the current README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except Exception as e:
        print(f"Error reading README: {e}")
        return False
    
    # Read the HackerRank stats
    try:
        with open(stats_path, 'r', encoding='utf-8') as f:
            hackerrank_content = f.read()
    except Exception as e:
        print(f"Error reading HackerRank stats: {e}")
        return False
    
    # Define the HackerRank section markers
    start_marker = "## 🏅 HackerRank Achievements"
    end_marker = "## 🔭 Current Focus"
    
    # Check if HackerRank section already exists
    if start_marker in readme_content:
        # Replace existing section
        pattern = f"({re.escape(start_marker)}.*?)({re.escape(end_marker)})"
        replacement = f"{start_marker}\n\n{hackerrank_content}\n{end_marker}"
        new_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    else:
        # Add new section after Competitive Programming section
        competitive_section = "## 🏆 Competitive Programming"
        
        if competitive_section in readme_content:
            # Find the end of the competitive programming section
            # Look for the next ## heading
            competitive_start = readme_content.find(competitive_section)
            if competitive_start != -1:
                # Find the next section
                next_section_match = re.search(r'\n## ', readme_content[competitive_start + len(competitive_section):])
                if next_section_match:
                    insertion_point = competitive_start + len(competitive_section) + next_section_match.start()
                    new_section = f"\n\n{start_marker}\n\n{hackerrank_content}\n"
                    new_readme = readme_content[:insertion_point] + new_section + readme_content[insertion_point:]
                else:
                    # Add at the end if no next section found
                    new_section = f"\n\n{start_marker}\n\n{hackerrank_content}\n"
                    new_readme = readme_content + new_section
            else:
                print("Could not find competitive programming section")
                return False
        else:
            print("Could not find competitive programming section")
            return False
    
    # Write the updated README
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_readme)
        print("README updated successfully")
        return True
    except Exception as e:
        print(f"Error writing updated README: {e}")
        return False

if __name__ == "__main__":
    success = update_readme()
    if success:
        print("README update completed")
    else:
        print("README update failed")
        exit(1)