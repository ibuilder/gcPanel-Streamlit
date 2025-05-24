#!/usr/bin/env python3
"""
Download sample construction plans for Highland Tower Development
"""

import requests
import os

def download_sample_plans():
    """Download the sample construction plan set from Kirkland WA"""
    
    # Create directory structure
    os.makedirs("data/documents/drawings", exist_ok=True)
    
    # Download the PDF
    url = "https://www.kirklandwa.gov/files/sharedassets/public/v/1/development-services/pdfs/building-pdfs/sample-construction-plan-set.pdf"
    
    try:
        print("Downloading sample construction plans...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the file
        output_path = "data/documents/drawings/Highland-Tower-Construction-Plans.pdf"
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"File size: {len(response.content)} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

if __name__ == "__main__":
    download_sample_plans()