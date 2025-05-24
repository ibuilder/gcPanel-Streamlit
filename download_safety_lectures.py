#!/usr/bin/env python3
"""
Download Construction Safety lectures for Highland Tower Development
"""

import requests
import os

def download_safety_lectures():
    """Download the construction safety lectures"""
    
    lectures = [
        {
            "name": "Building Construction Safety",
            "url": "https://mjobrien.com/podcasts/Lecture_Notes/Introduction_to_Construction_all_lecture_pdfs/2_Construction_Safety/D_Young_guest_lecture_building_construction.pdf",
            "filename": "building-construction-safety-lecture.pdf"
        },
        {
            "name": "Safety Overview",
            "url": "https://mjobrien.com/podcasts/Lecture_Notes/Introduction_to_Construction_all_lecture_pdfs/2_Construction_Safety/Safety_overview.pdf", 
            "filename": "safety-overview-lecture.pdf"
        }
    ]
    
    print("Downloading authentic construction safety lectures...")
    print("=" * 60)
    
    for lecture in lectures:
        try:
            print(f"Downloading {lecture['name']}...")
            response = requests.get(lecture['url'], timeout=30)
            response.raise_for_status()
            
            # Save the PDF content for reference
            output_path = f"data/references/{lecture['filename']}"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Successfully downloaded: {output_path}")
            print(f"   Content size: {len(response.content)} bytes")
            
        except Exception as e:
            print(f"❌ Error downloading {lecture['name']}: {e}")
            return False
    
    print("\n✅ All safety lectures downloaded successfully!")
    print("\nKey Safety Topics Covered:")
    print("🦺 Construction Safety Management:")
    print("  - OSHA compliance requirements")
    print("  - Fall protection systems")
    print("  - Personal protective equipment (PPE)")
    print("  - Hazard identification and analysis")
    print("  - Safety training and communication")
    print("  - Incident reporting and investigation")
    print("  - Safety planning and documentation")
    print("🏗️ Building Construction Safety:")
    print("  - High-rise construction safety")
    print("  - Structural safety considerations")
    print("  - Equipment and machinery safety")
    print("  - Site safety management")
    
    return True

if __name__ == "__main__":
    download_safety_lectures()