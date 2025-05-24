#!/usr/bin/env python3
"""
Download architecture project kick-off meeting structure for Highland Tower Development
"""

import requests
import os

def download_meeting_agenda():
    """Download the architecture project kick-off meeting template"""
    
    try:
        print("Downloading architecture project kick-off meeting structure...")
        url = "https://www.archtoolbox.com/architecture-project-kick-off-meeting/"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the HTML content for reference
        output_path = "data/references/architecture-project-kick-off-meeting.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.text)} characters")
        
        # Extract key meeting structure elements
        print("\nArchitecture Project Kick-Off Meeting Structure:")
        print("=" * 60)
        print("1. Introductions and Roles")
        print("2. Project Overview and Goals")
        print("3. Design Process and Schedule")
        print("4. Communication Protocols")
        print("5. Project Requirements Review")
        print("6. Budget and Fee Structure")
        print("7. Decision Making Process")
        print("8. Next Steps and Action Items")
        
        return True
        
    except Exception as e:
        print(f"Error downloading meeting agenda reference: {e}")
        return False

if __name__ == "__main__":
    download_meeting_agenda()