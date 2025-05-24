#!/usr/bin/env python3
"""
Download Construction Scheduling lecture for Highland Tower Development
"""

import requests
import os

def download_scheduling_lecture():
    """Download the construction scheduling lecture"""
    
    try:
        print("Downloading Construction Scheduling lecture...")
        url = "https://mjobrien.com/podcasts/Lecture_Notes/Introduction_to_Construction_all_lecture_pdfs/1b_Scheduling_and_Takeoff/Scheduling.pdf"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the PDF content for reference
        output_path = "data/references/construction-scheduling-lecture.pdf"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.content)} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error downloading scheduling lecture: {e}")
        return False

def download_project_delivery_lecture():
    """Download the project delivery forms lecture"""
    
    try:
        print("Downloading Project Delivery Forms lecture...")
        url = "https://mjobrien.com/podcasts/Lecture_Notes/Introduction_to_Construction_all_lecture_pdfs/1a_Project_Delivery/Forms_of_project_delivery.pdf"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the PDF content for reference
        output_path = "data/references/project-delivery-forms-lecture.pdf"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.content)} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error downloading project delivery lecture: {e}")
        return False

if __name__ == "__main__":
    print("Downloading authentic construction management lectures...")
    print("=" * 60)
    
    scheduling_success = download_scheduling_lecture()
    delivery_success = download_project_delivery_lecture()
    
    if scheduling_success and delivery_success:
        print("\n✅ All lectures downloaded successfully!")
        print("\nKey Topics Covered:")
        print("📅 Construction Scheduling:")
        print("  - CPM (Critical Path Method)")
        print("  - Project phases and milestones")
        print("  - Resource allocation and leveling")
        print("  - Schedule compression techniques")
        print("📋 Project Delivery Forms:")
        print("  - Project team roles and responsibilities") 
        print("  - Communication structures")
        print("  - Risk allocation frameworks")
        print("  - Contract relationships")
    else:
        print("\n❌ Some downloads failed. Please check network connection.")