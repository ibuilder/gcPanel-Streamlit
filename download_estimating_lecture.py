#!/usr/bin/env python3
"""
Download Takeoff and Estimating lecture for Highland Tower Development preconstruction module
"""

import requests
import os

def download_estimating_lecture():
    """Download the takeoff and estimating lecture"""
    
    try:
        print("Downloading Takeoff and Estimating lecture...")
        url = "https://mjobrien.com/podcasts/Lecture_Notes/Introduction_to_Construction_all_lecture_pdfs/1b_Scheduling_and_Takeoff/takeoff_shed_of_values_and_work_breakdown.pdf"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the PDF content for reference
        output_path = "data/references/takeoff-estimating-lecture.pdf"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.content)} bytes")
        
        print("\n📊 Construction Estimating - Key Components:")
        print("=" * 55)
        print("1. Quantity Takeoff Procedures")
        print("2. Work Breakdown Structure (WBS)")
        print("3. Material and Labor Pricing")
        print("4. Equipment Cost Analysis")
        print("5. Overhead and Profit Calculations")
        print("6. Risk and Contingency Planning")
        print("7. Bid Package Preparation")
        print("8. Cost Control Integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading estimating lecture: {e}")
        return False

if __name__ == "__main__":
    download_estimating_lecture()