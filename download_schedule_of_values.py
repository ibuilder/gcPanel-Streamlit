#!/usr/bin/env python3
"""
Download Sample Schedule of Values for Highland Tower Development contracts module
"""

import requests
import os

def download_schedule_of_values():
    """Download the sample schedule of values document"""
    
    try:
        print("Downloading Sample Schedule of Values...")
        url = "https://mjobrien.com/podcasts/Lecture_Notes/Introduction_to_Construction_all_lecture_pdfs/1b_Scheduling_and_Takeoff/SampleScheduleofValues.pdf"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the PDF content for reference
        output_path = "data/references/sample-schedule-of-values.pdf"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.content)} bytes")
        
        print("\n📋 Schedule of Values - Key Components:")
        print("=" * 50)
        print("1. Work Item Descriptions")
        print("2. Scheduled Values by Trade")
        print("3. Previous Progress Billing")
        print("4. Current Period Work Completed")
        print("5. Materials Presently Stored")
        print("6. Total Completed and Stored to Date")
        print("7. Percentage of Completion")
        print("8. Balance to Finish")
        print("9. Retainage Calculations")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading schedule of values: {e}")
        return False

if __name__ == "__main__":
    download_schedule_of_values()