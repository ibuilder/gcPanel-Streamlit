#!/usr/bin/env python3
"""
Download CSI MasterFormat Specification Divisions for Highland Tower Development
"""

import requests
import os

def download_csi_masterformat():
    """Download the CSI MasterFormat Specification Divisions PDF"""
    
    # Create directory structure
    os.makedirs("data/documents/specifications", exist_ok=True)
    
    # Download the PDF
    url = "https://mjobrien.com/MasterFormat_Specification_Divisions.pdf"
    
    try:
        print("Downloading CSI MasterFormat Specification Divisions...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the file
        output_path = "data/documents/specifications/CSI-MasterFormat-Specification-Divisions.pdf"
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"File size: {len(response.content)} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

if __name__ == "__main__":
    download_csi_masterformat()